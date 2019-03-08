import httplib2
import json
import logging

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger('Mode0')

def get_site_num():
    """Returns the identification number for the camera's site.
    """
    # TODO implement the actual site idenfification

    return '14'

def execute(sock):
    """Uses the socket to check in so the server knows the camera is alive.

    Arguments:
        sock - the socket to use
    """

    # first message indicates a request to check in
    message = 'alive'.encode('ascii')
    sock.sendall(message)
    logger.debug('Sent request to server...')

    sock_reply = sock.recv(4).decode('ascii')
    logger.debug('...received reply from server: {}'.format(sock_reply))

    if sock_reply == 'ACK':
        logger.debug('Server ACK\'d check-in request')
        message = get_site_num().encode('ascii')
        sock.sendall(message)
        logger.debug('Sent identification to server...')

        sock_reply = sock.recv(4).decode('ascii')
        logger.debug('...received reply from server: {}'.format(sock_reply))

        if sock_reply == 'ACK':
            logger.debug('Server ACK\'d site identification')
        else:
            logger.debug('Server didn\'t ACK site identification')
            # TODO handle failed identification
    else:
        logger.debug('Server didn\'t ACK check-in request')
        # TODO handle failed request

# code below to test just this module
#if __name__ == '__main__':

def execute2():
    httplib2.debuglevel = 0
    http = httplib2.Http()
    content_type_header = 'text/plain'
    url = "http://127.0.0.1:5000/TrailPiServer/api/v1.0/check_in"

    headers = {'Content-Type': content_type_header}
    data = {'site': get_site_num()}

    response, content = http.request(url, 'POST', json.dumps(data), headers = headers)
    logger.info('Response: {} + Content: {}'.format(response, content))
