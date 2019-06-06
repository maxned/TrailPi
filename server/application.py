from sys import version_info, exit
assert (version_info > (3, 6)), "Python 3.6 or later is required."
import logging
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import utils
import os
from werkzeug.utils import secure_filename
import activity
import json
import boto3
import datetime
import zipfile
import io
from models.views import db, Pictures, Tags, User
from auth.views import bcrypt, auth_blueprint

### CONSTANTS ###
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

### ENVIRONMENT VARIABLES ###
# AWS RDS configuration
username = os.environ.get('RDS_USERNAME')
password = os.environ.get('RDS_PASSWORD')
endpoint = os.environ.get('RDS_ENDPOINT')
instance = os.environ.get('RDS_INSTANCE')

# AWS S3 configuration
BUCKET_NAME = os.environ.get('BUCKET')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

### LOGGER ###
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('TrailServerMain')

### INITIALIZE APP ###
application = app = Flask(__name__) # needs to be named "application" for elastic beanstalk
CORS(app)

### INITIALIZE DATABASE CONNECTION
with app.app_context():
  db.init_app(app)
  
database_uri = f'mysql://{username}:{password}@{endpoint}/{instance}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.secret_key = 't_pi!sctkey%20190203#'

### INITIALIZE BCRYPT AND AUTH ###
with app.app_context():
  bcrypt.init_app(app)
app.register_blueprint(auth_blueprint)

### CUSTOM ROUTE UTILITIES ###
app.url_map.converters['list'] = utils.ListConverter

def is_allowed_site(site):
    """Returns whether passed site is valid

    Arguments:
        site - identification of the site checking in
    """
    try:
        site_as_int = int(site)
    except ValueError:
        logger.warning('Couldn\'t translate site to int')
        return False

    logger.debug('Site translated to: {}'.format(site_as_int))

    return 0 <= site_as_int <= 40

def is_allowed_file(filename):
    """Returns whether passed filename is valid

    Arguments:
        filename - name of the transferred file
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_matched_date(date, startDate, endDate):
  '''
    checks if a date falls within a given interval

    Arguments:
      date - the date to be checked
      startDate - 6 character string in format MMDDYY
      endDate - 6 character string in format MMDDYY
  '''
  if int(date, 10) >= int(startDate, 10) and int(date, 10) <= int(endDate, 10):
    return True

  return False

@app.route("/TrailPiServer/api/check_in", methods=['POST'])
def api_check_in():
    data = request.get_json()
    logger.debug('Data: {}'.format(data))

    if 'site' not in data:
        logger.warning('No site in request')
        response = jsonify({'status': 'Missing site field'})
        return response, 400

    site = data['site']
    logger.debug('Site: {}'.format(site))

    if site == '':
        logger.warning('Empty site in request')
        response = jsonify({'status': 'Missing site identification'})
        return response, 400

    if is_allowed_site(site):
        activity.check_in(site)
        response = jsonify({'status': 'OK'})
        return response, 200
    else:
        logger.warning('Invalid site in request')
        response = jsonify({'status': 'Invalid site'})
        return response, 400

    response = jsonify({'status': 'Unexpected error with request'})
    return response, 500

@app.route("/TrailPiServer/api/image_transfer", methods=['POST'])
def api_image_transfer():
    if 'file' not in request.files:
        logger.warning('Missing file field in POST')
        response = jsonify({'status': 'missing file field'})
        return response, 400

    if 'data' not in request.files:
        logger.warning('Missing data in POST')
        response = jsonify({'status': 'missing data field'})
        return response, 400

    file = request.files['file']
    data = json.load(request.files['data'])

    if 'site' not in data:
        logger.warning('Missing site in POST')
        response = jsonify({'status': 'missing site number'})
        return response, 400

    if file.filename == '':
        logger.warning('No selected file name in POST')
        response = jsonify({'status': 'missing file name'})
        return response, 400

    logger.debug('File: {}'.format(file))
    logger.debug('Data: {}'.format(data))

    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_name = filename[:-4] # strip filename extension
        image_time = datetime.datetime.strptime(image_name, '%m-%d-%y--%H-%M-%S-%f') # strip and format the timestamp
        bucket.Object(filename).put(Body=file)

        aws_s3_url = f'https://s3-us-west-2.amazonaws.com/{BUCKET_NAME}/{filename}'
        new_data = Pictures(site=data['site'], date=image_time, url=aws_s3_url)

        try:
            db.session.add(new_data)
            db.session.commit()
            db.session.close()
        except:
            logger.warning('Had to rollback during entry insertion')
            db.session.rollback()

        # retrieve picture id from uploaded image
        pic_entry = db.session.query(Pictures).filter(Pictures.url==aws_s3_url).first()

        # if the request has a tag, add it to the tags table
        if data['tag']:
          # create a new entry in the tags table
          new_entry = Tags(pic_id=pic_entry.pic_id, tag=data['tag'])

          try:
            db.session.add(new_entry)
            db.session.commit()
            db.session.close()
          except:
            logger.warning('Had to rollback during entry insertion')
            db.session.rollback()

        response = jsonify({'status': 'image upload SUCCESS'})
        return response, 200

    logger.warning('Unexpected error')
    response = jsonify({'status': 'unexpected error with request'})
    return response, 500

@app.route('/TrailPiServer/api/files', methods=['GET'])
def get_files():
  '''
    list all files inside of the S3 bucket
  '''
  s3_client = boto3.client(
      's3',
      aws_access_key_id=AWS_ACCESS_KEY,
      aws_secret_access_key=AWS_SECRET_KEY
  )
  files = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

  filenames = []
  for obj in files['Contents']:
    filenames.append(obj['Key'])

  response = jsonify({'filenames': filenames})
  return response, 200

@app.route('/TrailPiServer/api/download/<list:filenames>', methods=['GET'])
def download_files(filenames):
  '''
    retrieves a file from S3 and returns a Response object with
    "Content-Disposition: attachment", initiating a download from the user's browser
    Arguments:
      filenames: the list of files inside of the s3 bucket (filename extension included)
  '''
  s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY, 
    aws_secret_access_key=AWS_SECRET_KEY 
  )

  if len(filenames) == 1: # just download a single file
    filename = filenames[0]
    s3_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return Response(
      s3_response['Body'].read(),
      mimetype='text/plain',
      headers={"Content-Disposition": "attachment; filename={}".format(filename)}
    )
  else:
    zip_file = 'trailpi_images.zip'
    with zipfile.ZipFile(zip_file, 'w') as zipf:
      for filename in filenames:
        s3_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
        data = s3_response['Body'].read()
        with open(filename, 'wb') as file: # write the binary data to a file
          file.write(data)

        zipf.write(filename) # pack the file into a zipfile
        os.remove(filename)
       
    return send_file(
      zip_file, 
      attachment_filename='trailpi_images.zip', 
      as_attachment=True
    )

@app.route('/TrailPiServer/api/images/<startDate>/<endDate>/<list:requested_sites>', methods=['GET'])
def get_images(startDate, endDate, requested_sites):
  '''
    returns all of the images within the interval defined by startDate and endDate

    Arguments:
      startDate - 6 character string in MMDDYY format describing the start of the interval
      endDate - 6 character string in MMDDYY format describing the end of the interval
      requested_sites - list of sites in request
  '''
  results = db.session.query(Pictures).filter(Pictures.site.in_(requested_sites), Pictures.date >= startDate, Pictures.date <= endDate)

  imageInfo = []
  for record in results:
    tag_query = db.session.query(Tags).filter(Tags.pic_id == record.__dict__['pic_id'])
    tags = map(lambda tag_record: tag_record.__dict__['tag'], tag_query)
    imageInfo.append(
      {
        'id': record.__dict__['pic_id'],
        'site': record.__dict__['site'],
        'timestamp': record.__dict__['date'],
        'url': record.__dict__['url'],
        'tags': list(tags)
      }
    )

  response = jsonify({'images': imageInfo})
  return response, 200

@app.route('/TrailPiServer/api/tags/<image_id>/<list:tags>', methods=['POST'])
def add_tags(image_id, tags):
  auth_header = request.headers.get('Authorization')
  if auth_header:
    auth_token = auth_header.split(" ")[1]
  if auth_token:
    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, str): # if auth token is valid...
      for tag in tags: 
        new_entry = Tags(pic_id=image_id, tag=tag)
        db.session.add(new_entry)
        db.session.commit()

      response_object = {
        'status': 'success',
        'message': 'tags added successfully'
      }
      return jsonify(response_object), 200

  response_object = {
    'status': 'fail', 
    'message': 'Provide a valid auth token'
  }
  return jsonify(response_object), 401

# TODO - should probably be HTTP DELETE #
@app.route('/TrailPiServer/api/delete/<list:image_ids>', methods=['POST'])
def delete_images(image_ids):
  auth_header = request.headers.get('Authorization')
  logger.debug(f'Headers: {request.headers}')
  if auth_header:
    auth_token = auth_header.split(" ")[1]
  if auth_token:
    resp = User.decode_auth_token(auth_token)
    if not isinstance(resp, str): # if auth token is valid...
      s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY, 
        aws_secret_access_key=AWS_SECRET_KEY 
      )
      for image_id in image_ids: 
        result = db.session.query(Pictures).filter(Pictures.pic_id==image_id).first() # retrieve the image key from MySQL
        s3_key = result.url.split('/')[-1]
        db.session.query(Pictures).filter(Pictures.pic_id==image_id).delete() # delete the record from MySQL
        db.session.commit()
        s3_response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key) # delete the physical image from S3
        
      response_object = {
        'status': 'success',
        'message': 'requested images successfully deleted'
      }
      return jsonify(response_object), 200
      
  response_object = {
    'status': 'fail', 
    'message': 'Provide a valid auth token'
  }
  return jsonify(response_object), 401

if __name__ == '__main__':
  application.run()