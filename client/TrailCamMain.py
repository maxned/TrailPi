import sys
assert (sys.version_info > (3, 7)), "Python 3.7 or later is required."
import socket
import base64
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('TrailCamMain')

# helpful link for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

# FIXME just put host ip up here as global for testing ease, remove at some point
HOST_IP = '::1'

def make_connection(mode, image_data = None):
    """Connects to the server, then executes logic based on mode.

    Arguments:
        mode - what the connection will be used for
        image_data - optional, data for an image to transfer
    Modes:
        0: check in to show camera is active
        1: new image for transfer
    """

    # check for invalid mode, halt connection process
    if mode not in (0, 1):
        logger.warning('Invalid mode passed to make_connection')
        return

    logger.debug('Connecting to server...')

    # connect to the socket
    host = HOST_IP # FIXME see note on global variable
    port = 4567
    sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sock.connect((host,port))

    logger.debug('...connected!')

    # select logic and execute
    if mode == 0:
        import Mode0 as ClientLogic
        logger.debug('Executing logic with socket: {}'.format(sock))
        ClientLogic.execute(sock)

    elif mode == 1:
        import Mode1 as ClientLogic
        with open('test_image.png', 'rb') as image_file:
            image_data = base64.b64encode(image_file.read())
            logger.debug('Executing logic with socket: {} and image data: {}'.format(sock, image_data))
            ClientLogic.execute(sock, image_data)

    # done with socket, close it
    logger.info('Closing socket')
    sock.close()

def run_testing():
    """Loop that lets you set the mode for testing purposes.

    Inputs:
        None
    """

    print("Welcome to client testing!\n"
          "Modes:\n"
          "   0: Check-in\n"
          "   1: New image\n"
          "   123: quits testing")

    while True:
        mode = input('Which mode do you want to connect for? ')
        try:
            mode = int(mode)
        except ValueError:
            logger.warning('Input was not an int!')
            continue

        if mode == 123:
            logger.info('Quitting...')
            return

        make_connection(mode)

def main():
    # TODO implement logic for when to check-in and when to transfer an image

    run_testing()

if __name__ == '__main__':
    main()
