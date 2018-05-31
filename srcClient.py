"""
chat - client side - sends messages to others
"""

import socket
import sys
import msvcrt
import select

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2005
KEY_ENTER = 13
KEY_BACKSPACE = 8
PORT_INDEX = 1
SOCKET_RECV_BYTES = 1024


def main():
    """
    The program illustrates a chat system
    """
    try:
        my_socket = socket.socket()
        my_socket.connect((SERVER_IP, SERVER_PORT))
        my_msg = []
        socket_messages = []
        print 'client is connected to ({}) with port {}'.format(SERVER_IP, my_socket.getsockname()[PORT_INDEX])
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

            if msvcrt.kbhit():  # if the client typed character
                char = msvcrt.getch()  # get this character
                if chr(KEY_ENTER) is char:  # if enter
                    my_string_msg = ''.join(my_msg)
                    print '[Me]', my_string_msg
                    my_socket.send(my_string_msg)
                    my_msg = []  # clean array

                elif ord(char) == KEY_BACKSPACE:  # backspace
                    my_msg.pop()

                else:
                    # else just append the character to the message
                    my_msg.append(char)
    except Exception as e:
        print 'Exception occurred, value:', e
    finally:
        my_socket.close()
        print 'client connection is closed'


if __name__ == "__main__":
    main()
