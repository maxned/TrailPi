from sys import version_info
assert (version_info > (3, 7)), "Python 3.7 or later is required."
import logging
from flask import Flask, request
import mysql.connector
from mysql.connector import errorcode
import os
from werkzeug.utils import secure_filename
import Living

def allowed_site(site):
    """Returns whether passed site is valid

    Arguments:
        site - identification of the site checking in
    """
    try:
        as_int = int(site)
    except ValueError:
        logger.warning('Couldn\'t translate site to int')
        return False

    return 0 <= as_int <= 40

def allowed_file(filename):
    """Returns whether passed filename is valid

    Arguments:
        filename - name of the transferred file
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def message_received(methods = ['GET', 'POST']):
    """Logs that a message was received

    Arguments:
        None
    """

    logger.info('Message was received!')
    return

@app.route("/")
def home():
    return "Hello World"

@app.route("/TrailPiServer/api/check_in", methods=['POST'])
def api_checkin():
    if 'site' not in request.data:
        logger.warning('No site part in request')
        return 'Missing site', 400

    if request.headers['Content-Type'] != 'text/plain':
        logger.warning('Unsupported data type')
        return 'Unsupported data type', 415

    site = request.data['site']

    if site == '':
        logger.warning('Empty site in request')
        return 'Missing site', 400

    if allowed_site(site):
        logger.info('Request data: {}'.format(request.data))

        Living.check_in(request.data)

        return 'OK', 200

    return 'Unexpected error with request', 400

@app.route("/TrailPiServer/api/image_transfer", methods=['POST'])
def api_image_transfer():
    if 'file' not in request.files:
        logger.warning('No file part in request')
        return 'Missing file', 400

    file = request.files['file']

    if file.filename == '':
        logger.warning('No selected file name')
        return 'Missing filename', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # TODO dynamically determine a save location
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        mycursor = myDB.cursor()

        sql = 'INSERT INTO Images (name, path) VALUES (%s, %s)'
        val = [(filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))]

        mycursor.executemany(sql, val)
        myDB.commit()

        return 'OK', 200

    return 'Unexpected error with request', 400

UPLOAD_FOLDER = '/home/brody/GitHub/TrailPi/server/uploaded_images' # FIXME not the actual path
ALLOWED_EXTENSIONS = set(['png']) # TODO support more extensions?

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('TrailServerMain')

app = Flask(__name__)
app.secret_key = b't_pi!sctkey%20190203#'

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

app.run(debug = True)
