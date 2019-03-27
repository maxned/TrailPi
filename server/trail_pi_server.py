from sys import version_info, exit
assert (version_info > (3, 6)), "Python 3.7 or later is required."
import logging
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
import os
from werkzeug.utils import secure_filename
import activity
import json

UPLOAD_FOLDER = '/home/brody/GitHub/TrailPi/server/uploaded_images' # FIXME not the actual path
ALLOWED_EXTENSIONS = set(['png']) # TODO support more extensions?

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('TrailServerMain')

app = Flask(__name__)
app.secret_key = 't_pi!sctkey%20190203#'
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

@app.route("/TrailPiServer/api/check_in", methods=['POST'])
def api_check_in():
    '''if 'site' not in request.data:
        logger.warning('No site in request')
        return jsonify({'status': 'Missing site field'}), 400

    if request.headers['Content-Type'] != 'application/json':
        logger.warning('Unsupported data type in request')
        return jsonify({'status': 'Unsupported data type'}), 415'''

    data = request.get_json()
    site = data['site']
    logger.debug('Data: {}'.format(data))

    logger.debug('Site: {}'.format(site))

    if site == '':
        logger.warning('Empty site in request')
        return jsonify({'status': 'Missing site identification'}), 400

    if is_allowed_site(site):
        activity.check_in(site)

        return jsonify({'status': 'OK'}), 200
    else:
        logger.warning('Invalid site in request')
        return jsonify({'status': 'Invalid site'}), 400

    return jsonify({'status': 'Unexpected error with request'}), 400

@app.route("/TrailPiServer/api/image_transfer", methods=['POST'])
def api_image_transfer():
    #logger.debug('Data: {}'.format(request.data))
    #logger.debug('Files: {}'.format(request.files))

    '''if 'file' not in request.data:
        logger.warning('No file in request')
        return 'Missing file field', 400'''

    '''if b'site' not in request.data:
        logger.warning('No site in request')
        return 'Missing site field', 400'''

    '''if request.headers['Content-Type'] != 'image/png' or request.headers['Content-Type'] != 'image/jpg':
        logger.warning('Unsupported data type in request')
        return 'Unsupported data type', 415'''

    if 'file' not in request.files: 
        return jsonify({'status': 'no file found'}), 400

    for item in request.files:
        logger.debug(item)

    data = request.files['data']
    file = request.files['file']
    site = data['site']

    #data = request.get_json()
    #site = data['site']
    #site = request.data.decode()[5:] # data comes through as 'site=##'
    logger.debug('File: {}'.format(file))
    logger.debug('Site: {}'.format(site))

    if file.filename == '':
        logger.warning('No selected file name')
        return 'Missing filename', 400

    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # TODO dynamically determine a save location
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        """mycursor = myDB.cursor()

        sql = 'INSERT INTO Images (name, path) VALUES (%s, %s)'
        val = [(filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))]

        mycursor.executemany(sql, val)
        myDB.commit()"""

        return jsonify({'status': 'OK'}), 200

    logger.warning('Unexpected error')
    return 'Unexpected error with request', 400

if __name__ == "__main__":
    app.run(debug = True)
