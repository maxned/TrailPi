import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Mode1')

def execute(sock, image_data):
    """Uses the socket to transfer a new image to the server.

    Arguments:
        sock - the socket to use
        image_data - the data for the image to transfer
    """

    # first message indicates a request to transfer an image
    message = 'image'.encode('ascii')
    sock.sendall(message)
    logger.debug('Sent request to server...')

    sock_reply = sock.recv(4).decode('ascii')
    logger.debug('...received reply from server: {}'.format(sock_reply))

    if sock_reply == 'ACK':
        logger.debug('Server ACK\'d transfer request')
        sock.sendall(image_data)
        logger.debug('Sent image to server...')

        sock_reply = sock.recv(4).decode('ascii')
        logger.debug('...received reply from server: {}'.format(sock_reply))

        if sock_reply == 'ACK':
            logger.debug('Server ACK\'d image transfer')
        else:
            logger.debug('Server didn\'t ACK image transfer')
            # TODO handle a failed transfer
    else:
        logger.debug('Server didn\'t ACK transfer request')
        # TODO handle failed request

# code below to test just this module
#if __name__ == '__main__':
