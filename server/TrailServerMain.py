import sys
assert (sys.version_info > (3, 7)), "Python 3.7 or later is required."
import socket
import threading
import Living
import base64
import time
import logging

from flask import Flask, request, json
import mysql.connector
from mysql.connector import errorcode

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('TrailServerMain')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tpisctkey20190203'

try:
    myDB = mysql.connector.connect(user = 'TrailPiAdmin', host = 'localhost',
                                   password = 'tmppw', database = 'TrailPiImages')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.warning('Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.warning('Database does not exist')
    else:
        logger.warning('Encountered error: {}'.format(err))

# FIXME just put host ip up here as global for testing ease, remove when unnecessary
HOST_IP = '::1'

# helpful links for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client/23828265#23828265

def acknowledge(cli):
    """Send an ACK to the passed client.

    Arguments:
        cli - client to send the ACK to
    """
    cli.sendall('ACK'.encode('ascii'))

def log_request(msg):
    """Logs the passed msg request to a file.

    Arguments:
        msg - the request to log
    """
    with open('received_requests.log', 'a+') as log_file:
        logger.info('Logging request to file')
        log_file.write("{0:25} {1}\n".format(time.strftime('%X %x %Z'), msg))

def thread_main(cli, addr):
    """Main logic to be performed for the clients.

    Arguments:
        cli - socket to communicate over
        addr - connected address
    """

    cli.settimeout(60) # times out after 60s of no sending
    while True:
        logger.info('Trying to receive')
        try:
            # receive first message from client that identifies request type
            data = cli.recv(5).decode('ascii')
            logger.debug('Received data: \'{}\''.format(data))

            if not data:
                logger.info('Connection closed by client, closing socket & thread')
                cli.close()
                return
        except socket.timeout as err:
            logger.info('Client timed out, closing socket & thread: {}'.format(err))
            cli.close()
            return
        except:
            logger.warning('Unexpected error')
            cli.close()
            return

        if data == 'alive':
            logger.debug('Client sent a check-in request')
            log_request(data)

            # send ACK to client
            acknowledge(cli)

            # listen for site identification
            try:
                # receive second message from client that identifies site
                data = cli.recv(2).decode('ascii')

                if not data:
                    logger.info('Connection closed by client, closing socket & thread')
                    cli.close()
                    return
            except socket.timeout as err:
                logger.info('Client timed out, closing socket & thread: {}'.format(err))
                cli.close()
                return
            except:
                logger.warning('Unexpected error')
                cli.close()
                return

            log_request(data)

            # send ACK to client
            acknowledge(cli)

            logger.debug('Site {} has checked in and is alive'.format(data))
            Living.check_in(data)

        elif data == 'image':
            logger.debug('Client sent an image transfer request')
            log_request(data)

            # send ACK to client
            acknowledge(cli)

            # listen for image data
            try:
                data = cli.recv(4096) # TODO is this size enough?

                if not data:
                    logger.info('Connection closed by client, closing socket & thread')
                    cli.close()
                    return
            except socket.timeout as err:
                logger.info('Client timed out, closing socket & thread: {}'.format(err))
                cli.close()
                return
            except:
                logger.warning('Unexpected error')
                cli.close()
                return

            log_request(data)

            # send ACK to client
            acknowledge(cli)

            logger.debug('Client transferred data {}'.format(data))
            # TODO implement logic to save image on filesystem and add to MySQL database

            # example data string to image:
            image_file = open("test_image.png", "wb")
            image_file.write(base64.b64decode(data))
            image_file.close()

        elif data != '':
            # TODO handle unknown request type?
            log_request(data)
            logger.warning('Unhandled request type, closing socket & thread')
            cli.close()
            return

def main():
    host = HOST_IP
    port = 4567
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind((host, port))
    logger.info('Socket bound to port {}'.format(port))

    # listen on socket
    sock.listen(10)
    logger.info('Socket listening for clients')

    # wait until client wants to exit
    while True:
        # accept client
        cli, addr = sock.accept()

        # start a new thread for client
        logger.debug('Starting thread for new client')
        threading.Thread(target = thread_main, args = (cli, addr)).start()

@app.route("/")
def home():
    return "Hello World"

@app.route("/TrailPiServer/api/v1.0/check_in", methods=['POST'])
def api_checkin():
    if request.headers['Content-Type'] == 'text/plain':
        logger.info('Request data: {}'.format(request.data))

        # TODO interact with living

        return 'OK', 200
    else:
        logger.warning('Unsupported data type')
        return 'Unsupported data type', 415

@app.route("/TrailPiServer/api/v1.0/image_transfer", methods=['POST'])
def api_image_transfer():
    if request.headers['Content-Type'] == 'image/png':
        logger.info('Request data: {}'.format(request.data))

        mycursor = myDB.cursor()

        sql = 'INSERT INTO Images (name, path) VALUES (%s, %s)'
        val = [('name1', 'path1'),
               ('name2, path2')]

        mycursor.executemany(sql, val)
        myDB.commit()

        return 'OK', 200
    else:
        logger.warning('Unsupported data type')
        return 'Unsupported data type', 415

def messageReceived(methods = ['GET', 'POST']):
    logger.info('Message was received!')

if __name__ == '__main__':
    #main()
    app.run(debug = True)
