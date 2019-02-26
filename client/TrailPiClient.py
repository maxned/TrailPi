import socket

# enforce version
MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# helpful link for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

if __name__ == '__main__':
    host = '2601:203:480:17d8:196d:2760:13fe:127e'
    port = 4567
    sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sock.connect((host,port))

    # message to send - TODO fill out
    message = "Just a filler message for now"

    while True:
        # send data
        sock.send(message.encode('ascii'))

        # received verification
        data = sock.recv(1024)

        if data == 'ACK':
            print('Received ACK')
        break

    # close the connection
    sock.close()
