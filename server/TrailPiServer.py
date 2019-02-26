#!/usr/bin/python3.7
import sys
import socket
import threading

# enforce version
MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# mutex for locking per client
CLIENT_LOCK = threading.Lock()

# helpful link for threaded python3 ipv6 server script
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

def threadMain(cli):
    while True:
        # received from client
        data = cli.recv(1024)
        if not data:
            print('Closing client')
            CLIENT_LOCK.release()
            break

        # send ACK to client
        cli.send('ACK')

    # connection closed
    cli.close()

if __name__ == '__main__':
    host = "2601:203:480:17d8:196d:2760:13fe:127e"
    port = 4567
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.bind((host, port))
    print("Socket bound to port ", port)

    # listen on socket
    sock.listen(10)
    print("Socket listening for clients")

    # wait until client wants to exit
    while True:
        # accept client
        cli, addr = sock.accept()

        # lock before proceeding
        CLIENT_LOCK.acquire()
        print('Connected to client: ', addr[0], ':', addr[1])

        # Start a new thread for client
        start_new_thread(threadMain, (cli,))

    sock.close()
