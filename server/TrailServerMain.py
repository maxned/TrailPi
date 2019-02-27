import sys
import socket
import threading

# FIXME just put host ip up here as global for testing ease, remove when unnecessary
HOST_IP = '::1'

assert (sys.version_info > (3, 7)), "Python 3.7 or later is required."

# helpful links for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client/23828265#23828265

def acknowledge(cli):
    """Send an ACK to the passed client.

    Arguments:
        cli - client to send the ACK to
    """
    cli.send('ACK'.encode('ascii'))

def thread_main(cli, addr):
    """Main logic to be performed for the clients.

    Arguments:
        cli - socket to communicate over
        addr - connected address
    """

    while True:
        try:
            # receive first message from client that identifies request type
            data = cli.recv(6).decode('ascii')
            if data:
                print('Received data:', data) # DEBUG debugging output

                if data == 'alive':
                    print('Client sent a check-in request') # DEBUG debugging output

                    # send ACK to client
                    acknowledge(cli)

                    # listen for site identification
                    data = cli.recv(2).decode('ascii')
                    if data:
                        print('Site', data, 'has checked in and is alive') # DEBUG debugging output
                        # TODO implement logic to track sites that are alive

                        # send ACK to client
                        acknowledge(cli)

                elif data == 'image':
                    print('Client sent an image transfer request') # DEBUG debugging output

                    # send ACK to client
                    acknowledge(cli)

                    # listen for image data
                    data = cli.recv(4096).decode('ascii') # TODO is this size enough?
                    if data:
                        print('Client transferred data:', data) # DEBUG debugging output
                        # TODO implement logic to save image and add to database

                        # send ACK to client
                        acknowledge(cli)

                        # data string to image:
                        image_file = open("test_image.png", "wb")
                        image_file.write(data.decode('base64'))
                        image_file.close()

                else:
                    print('Unhandled request type')
                    # TODO handle unknown request type?

        except:
            # close connection
            print('Client timed out, closing')
            cli.close()
            return False

def main():
    host = HOST_IP
    port = 4567
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind((host, port))
    print('Socket bound to port', port)

    # listen on socket
    sock.listen(10)
    print('Socket listening for clients')

    # wait until client wants to exit
    while True:
        # accept client
        cli, addr = sock.accept()
        cli.settimeout(60) # times out after 60s of no sending TODO test if working

        # start a new thread for client
        print('Starting thread for new client') # DEBUG debugging output
        threading.Thread(target = thread_main, args = (cli, addr)).start()


if __name__ == '__main__':
    main()
