import sys
import socket

# FIXME just put host ip up here as global for testing ease, remove when unnecessary
HOST_IP = '::1'

# enforce version
MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# helpful link for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

def check_in(sock):
    """
    check_in: Uses the socket to check in so the server knows the camera is alive.
    Inputs:
        sock - the socket to use
    """
    # first message indicates a request to check in
    message = 'alive'
    sock.send(message.encode('ascii'))

    sock_reply = sock.recv(4)
    print('Received reply from server: ', sock_reply) # DEBUG debugging output

    if sock_reply.upper() == 'ACK':
        # TODO implement the actual site idenfification

        print('Server ACK\'d check-in request') # DEBUG debugging output
        message = '14' # DEBUG pretend to send site identification
        sock.send(message.encode(ascii))

        sock_reply = sock.recv(4)
        if sock_reply.upper() == 'ACK':
            print('Server ACK\'d site check-in') # DEBUG debugging output
        else:
            # TODO handle failed identification
            print('Server didn\'t ACK site check-in') # DEBUG debugging output
        # TODO implement the actual site identification
    else:
        # TODO handle failed request
        print('Server didn\'t ACK check-in request') # DEBUG debugging output

def new_image(sock, image_data):
    """
    new_image: Uses the socket to transfer a new image to the server.
    Inputs:
        sock - the socket to use
        image_data - the data for the image to transfer
    """
    # first message indicates a request to transfer an image
    message = 'image'
    sock.send(message.encode('ascii'))

    sock_reply = sock.recv(4)
    print('Received reply from server: ', sock_reply) # DEBUG debugging output

    if sock_reply.upper() == 'ACK':
        # TODO implement the actual image transfer

        print('Server ACK\'d transfer request') # DEBUG debugging output
        message = image_data or 'No data' # DEBUG pretend to send image data
        sock.send(message.encode('ascii'))

        sock_reply = sock.recv(4)
        if sock_reply.upper() == 'ACK':
            print('Server ACK\'d image transfer') # DEBUG debugging output
        else:
            # TODO handle a failed transfer
            print('Server didn\'t ACK image transfer') # DEBUG debugging output
        # DEBUG pretend to send image data

    else:
        # TODO handle failed request
        print('Server didn\'t ACK transfer request') # DEBUG debugging output

def make_connection(mode, image_data = None):
    """
    make_connection: Establishes a connection between the client and the server then calls logic function based on mode.
    Inputs:
        mode - what mode the connection will be used for
        image_data - if a new image is being transferred to the server, this will contain the appropriate data
    Modes:
        0: checks in so the server knows the client is active
        1: client has a new image to transfer to the server
    """

    # check for invalid mode, halt connection process
    if mode not in [0, 1]:
        print('Invalid mode passed to make_connection')
        return

    # connect to the socket
    host = HOST_IP # FIXME see note on global variable
    port = 4567
    sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sock.connect((host,port))

    # execute based on mode
    if mode == 0:
        check_in(sock)
    elif mode == 1:
        new_image(sock, image_data)

    # done with socket, close it
    sock.close()

def main():
    # TODO implement logic for when to check-in and when to transfer an image

    # DEBUG loop and set mode for testing purposes
    while True:
        mode = input('What mode to connect for? 123 to quit: ')
        try:
            mode = int(mode)
        except ValueError:
            print('Input was not an int!')
            continue

        if mode == 123:
            print('Quitting...')
            return

        print('Entered client main - connecting for mode: ', mode)
        make_connection(mode)
    # DEBUG loop and set mode for testing purposes

if __name__ == '__main__':
    main()
