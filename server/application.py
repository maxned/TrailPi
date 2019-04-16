from sys import version_info, exit
assert (version_info > (3, 6)), "Python 3.7 or later is required."
import logging
from flask import Flask, request, jsonify
#import mysql.connector
#from mysql.connector import errorcode
import os
from werkzeug.utils import secure_filename
import activity
import json
import boto3

UPLOAD_FOLDER = '/home/brody/GitHub/TrailPi/server/uploaded_images' # FIXME not the actual path
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) # TODO support more extensions?

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('TrailServerMain')

application = app = Flask(__name__) # needs to be named "application" for elastic beanstalk
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

"""
try:
    # TODO set more permanent information
    myDB = mysql.connector.connect(user = 'TrailPiAdmin', host = 'localhost',
                                  password = 'tmppw', database = 'TrailPiImages')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.error('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.error('Database does not exist')
    else:
        logger.error('Encountered error: {}'.format(err))
    exit()
"""
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
  if int(date, 10) >= int(startDate, 10) and int(date, 10) <= (endDate, 10):
    return True
  
  return False


@app.route("/TrailPiServer/api/check_in", methods=['POST'])
def api_check_in():
    ''' TODO -> check for content-type?? '''

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
    ''' TODO -> check for content-type?? '''

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

        # TODO dynamically determine a save location
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        """mycursor = myDB.cursor()

        sql = 'INSERT INTO Images (name, path) VALUES (%s, %s)'
        val = [(filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))]

        mycursor.executemany(sql, val)
        myDB.commit()"""

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

if __name__ == '__main__':
    application.run(debug = True)

@app.route('/TrailPiServer/api/filesByDateRange?startDate=<startDate>&endDate=<endDate>', methods=['GET'])
def get_files_by_date_range(startDate, endDate):
  ''' 
    returns all of the images within the interval defined by startDate and endDate

    Arguments: 
      startDate - 6 character string in MMDDYY format describing the start of the interval
      endDate - 6 character string in MMDDYY format describing the end of the interval
  '''
  client = boto3.client(
    's3'
    aws_access_key_id=AWS_ACCESS_KEY 
    aws_secret_access_key=AWS_SECRET_KEY 
  )
  files = client.list_objects_v2(Bucket=BUCKET_NAME)

  filenames = []  
  for obj in files['Contents']:
    filename = obj['Key']
    if is_matched_date(filename[0:5]):
      filenames.append(filename)

  response = jsonify({'filenames': filenames})
  return response, 200
