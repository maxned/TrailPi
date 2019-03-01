def execute(sock, image_data):
    """Uses the socket to transfer a new image to the server.

    Arguments:
        sock - the socket to use
        image_data - the data for the image to transfer
    """

    # first message indicates a request to transfer an image
    message = 'image'.encode('ascii')
    sock.sendall(message)
    print('Sent request to server...') # DEBUG debugging output

    sock_reply = sock.recv(4).decode('ascii')
    print('...received reply from server:', sock_reply) # DEBUG debugging output

    if sock_reply == 'ACK':
        # TODO implement the actual image transfer

        print('Server ACK\'d transfer request') # DEBUG debugging output
        message = image_data # DEBUG pretend to send image data
        sock.sendall(message)
        print('Sent image to server...') # DEBUG debugging output

        sock_reply = sock.recv(4).decode('ascii')
        print('...received reply from server:', sock_reply) # DEBUG debugging output

        if sock_reply == 'ACK':
            print('Server ACK\'d image transfer') # DEBUG debugging output
        else:
            print('Server didn\'t ACK image transfer') # DEBUG debugging output
            # TODO handle a failed transfer
    else:
        print('Server didn\'t ACK transfer request') # DEBUG debugging output
        # TODO handle failed request

# code below to test just this module
#if __name__ == '__main__':
