"""
chat - server side - deliver the messages to clients
"""

import socket
import select
import sys

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2005
PORT_INDEX = 1
SOCKET_RECV_BYTES = 1024
SOCKET_LISTEN = 5

open_client_sockets = []
messages_to_send = []


def send_waiting_messages(list):
    """
    The function sends messages that need to be sent only if the client is writeable
    :param list: writeable clients
    """
    messages_to_remove = []
    for message in messages_to_send:
        (client_socket, data) = message
        for wsocket in list:
            if wsocket is not client_socket:
                wsocket.send('[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], data))
        messages_to_remove.append(message)
    for message_remove in messages_to_remove:
        messages_to_send.remove(message_remove)


def main():
    """
    The program illustrates a server who receives data from multiple clients and replies
    """
    try:
        server_socket = socket.socket()
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(SOCKET_LISTEN)
        print 'server({}) is up. listening in port {}'.format(SERVER_IP, SERVER_PORT)
        while True:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
            for current_socket in rlist:
                if current_socket is server_socket:
                    (new_socket, address) = server_socket.accept()
                    open_client_sockets.append(new_socket)
                else:
                    try:
                        print '.....New data from client.....'
                        data = current_socket.recv(SOCKET_RECV_BYTES)
                        if data == "":
                            open_client_sockets.remove(current_socket)
                            print "Connection with client closed."
                        else:
                            messages_to_send.append((current_socket, data))
                    except Exception as e:
                        if current_socket in open_client_sockets:
                            open_client_sockets.remove(current_socket)
                        print 'Exception occurred in receive, value:', e.message
            send_waiting_messages(wlist)

    except Exception as e:
        print 'Exception occurred, value:', e.message
    finally:
        server_socket.close()
        print 'server connection is closed'


if __name__ == "__main__":
    main()
