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

        # TODO dynamically determine a save location
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        """mycursor = myDB.cursor()

        sql = 'INSERT INTO Images (name, path) VALUES (%s, %s)'
        val = [(filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))]

        mycursor.executemany(sql, val)
        myDB.commit()"""

        response = jsonify({'status': 'OK'})
        return response, 200

    logger.warning('Unexpected error')
    response = jsonify({'status': 'unexpected error with request'})
    return response, 500

if __name__ == "__main__":
    app.run(debug = True)
