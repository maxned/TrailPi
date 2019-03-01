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
    print('Sent request to server...') # DEBUG debugging output

    sock_reply = sock.recv(4).decode('ascii')
    print('...received reply from server:', sock_reply) # DEBUG debugging output

    if sock_reply == 'ACK':
        print('Server ACK\'d check-in request') # DEBUG debugging output
        message = get_site_num().encode('ascii')
        sock.sendall(message)
        print('Sent identification to server...') # DEBUG debugging output

        sock_reply = sock.recv(4).decode('ascii')
        print('...received reply from server:', sock_reply) # DEBUG debugging output

        if sock_reply == 'ACK':
            print('Server ACK\'d site identification') # DEBUG debugging output
        else:
            print('Server didn\'t ACK site identification') # DEBUG debugging output
            # TODO handle failed identification
    else:
        print('Server didn\'t ACK check-in request') # DEBUG debugging output
        # TODO handle failed request

# code below to test just this module
#if __name__ == '__main__':
