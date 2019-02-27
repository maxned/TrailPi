#!/usr/bin/python3.7
import sys
import socket
from threading import Thread

# FIXME just put host ip up here as global for testing ease, remove when unnecessary
HOST_IP = '::1'

# enforce version
MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# mutex for locking per client
CLIENT_LOCK = threading.Lock()

# helpful link for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

def thread_main(cli):
    """
    thread_main: Main logic to be performed for the clients
    """
    while True:
        # receive first message from client that identifies request type
        data = cli.recv(6)
        if not data:
            print('Closing client')
            CLIENT_LOCK.release()
            break

        if data.lower() == 'alive':
            print('Client is alive') # DEBUG debugging output
            # send ACK to client
            cli.send('ACK'.encode('ascii'))

            # listen for site identification
            data = cli.recv(2)
            if not data:
                # TODO handle failure to get site ID
                print('Err getting site ID')
                break
            print('Site ', data, ' has check-in and is alive') # DEBUG debugging output
            # TODO implement logic to track sites that are alive
            cli.send('ACK'.encode('ascii'))

        elif data.lower() == 'image':
            print('Client has a new image to transfer') # DEBUG debugging output
            # send ACK to client
            cli.send('ACK'.encode('ascii'))

            # listen for image data
            data = cli.recv(4096)
            if not data:
                # TODO handle failure to get image data
                print('Err getting image data')
                break
            print('Client transferred data: ', data) # DEBUG debugging output
            cli.send('ACK'.encode('ascii'))

        else:
            # TODO handle this?
            print('Unhandled request type')

    # close connection
    CLIENT_LOCK.release()
    cli.close()

def main():
    host = HOST_IP
    port = 4567
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind((host, port))
    print('Socket bound to port ', port)

    # listen on socket
    sock.listen(10)
    print('Socket listening for clients')

    # wait until client wants to exit
    while True:
        # accept client
        cli, addr = sock.accept()

        # lock before proceeding
        CLIENT_LOCK.acquire()
        print('Connected to client: ', addr[0], ':', addr[1])

        # Start a new thread for client
        thread = Thread(target = thread_main, args = (cli,))
        thread.start()
        thread.join()

    sock.close()


if __name__ == '__main__':
    main()
