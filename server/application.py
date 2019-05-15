from sys import version_info, exit
assert (version_info > (3, 6)), "Python 3.6 or later is required."
import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, DATETIME
import utils
import os
from werkzeug.utils import secure_filename
import activity
import json
import boto3
import datetime

UPLOAD_FOLDER = '/home/brody/GitHub/TrailPi/server/uploaded_images' # FIXME not the actual path
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) # TODO: support more extensions?

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('TrailServerMain')

application = app = Flask(__name__) # needs to be named "application" for elastic beanstalk
CORS(app)
app.secret_key = 't_pi!sctkey%20190203#'

# MySQL database initialization
username = os.environ.get('RDS_USERNAME')
password = os.environ.get('RDS_PASSWORD')
endpoint = os.environ.get('RDS_ENDPOINT')
instance = os.environ.get('RDS_INSTANCE')
database_uri = f'mysql://{username}:{password}@{endpoint}/{instance}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)
app.url_map.converters['list'] = utils.ListConverter
app.secret_key = 't_pi!sctkey%20190203#' 

# AWS S3 configuration
BUCKET_NAME = os.environ.get('BUCKET')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

s3 = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)
bucket = s3.Bucket(BUCKET_NAME)

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
    ''' TODO: -> check for content-type?? '''

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
    ''' TODO: -> check for content-type?? '''

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
        bucket.Object(filename).put(Body=file)

        aws_s3_url = f'https://s3-us-west-2.amazonaws.com/{BUCKET_NAME}/{filename}'
        new_data = Pictures(site=data['site'], date=utils.get_local_date(), url=aws_s3_url)

        try:
            db.session.add(new_data)
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

# TODO: find a way to do this with boto3 resource instead of client
@app.route('/TrailPiServer/api/files', methods=['GET'])
def get_files():
  '''
    list all files inside of the S3 bucket
  '''
  client = boto3.client(
      's3',
      aws_access_key_id=AWS_ACCESS_KEY,
      aws_secret_access_key=AWS_SECRET_KEY
  )
  files = client.list_objects_v2(Bucket=BUCKET_NAME)

  filenames = []
  for obj in files['Contents']:
    filenames.append(obj['Key'])

  response = jsonify({'filenames': filenames})
  return response, 200

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
    imageInfo.append(
      {
        'site': record.__dict__['site']
        'timestamp': record.__dict__['date'], 
        'url': record.__dict__['url']
      }
    )

  response = jsonify({'images': imageInfo})
  return response, 200

@app.route('/TrailPiServer/api/downloadFile/<filename>', methods=['GET'])
def download_file(filename):
  '''
    retrieves a file from S3 and returns a Response object with
    "Content-Disposition: attachment", initiating a download from the user's browser

    Arguments:
      filename: the name of the file inside of the s3 bucket (filename extension included)
  '''
  s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY, 
    aws_secret_access_key=AWS_SECRET_KEY 
  )
  file = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
  return Response (
    file['Body'].read(),
    mimetype='text/plain',
    headers={"Content-Disposition": "attachment; filename={}".format(filename)}
  )

# SQL Models
# TODO -> move these to another file. This is just for an elastic beanstalk test

class Pictures(db.Model):
  """Represents an entry for the Pictures table
  """
  __tablename__ = 'Pictures'

  pic_id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
  site = db.Column(TINYINT(display_width=2, unsigned=True), nullable=False)
  date = db.Column(DATETIME, default=utils.get_local_date(), nullable=False)
  url = db.Column(db.String(200), nullable=False)
  tags = db.relationship('Tags', backref='picture', lazy=True)

  def __init__(self, site, date, url):
    self.site = site
    self.date = date
    self.url = url

  def __repr__(self):
    return '<Picture(%r, %r, %r)>' % (self.site, self.date, self.url)

class Tags(db.Model):
  """Represents an entry for the Tags table
  """
  __tablename__ = 'Tags'

  pic_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('Pictures.pic_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
  tag = db.Column(db.String(length=20), primary_key=True)

  def __init__(self, pic_id, tag):
    self.pic_id = pic_id
    self.tag = tag

  def __repr__(self):
    return '<Tag(%r, %r)>' % self.id, self.tag

if __name__ == '__main__':
  application.run(debug = True)