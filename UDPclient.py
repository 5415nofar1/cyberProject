import socket

msgFromClient = "0"
bytesToSend = str.encode(msgFromClient)
SERVER_ADDR = ("127.0.0.1", 20001)
bufferSize = 1024


def func1():
    print 1
    return 1


def func2():
    print 2
    return 2


action_dict = {
    1: func1,
    2: func2
}


def action_to_preform(decrypt_message):
    action_code = int(decrypt_message)
    return action_dict[action_code]()


def manipulate_message(encrypt_message):
    decrypt_message = decryption(encrypt_message)
    return action_to_preform(decrypt_message)


def decryption(message):
    return message


def main():
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.connect(SERVER_ADDR)

    # Send to server using created UDP socket
    UDPClientSocket.send(bytesToSend)

    msgFromServer = UDPClientSocket.recv(bufferSize)
    print("ACK from Attacker {}".format(msgFromServer[0]))

    while True:
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
        message = bytesAddressPair
        print("Message from Attacker:{}".format(message))

        manipulate_message(message)

        UDPClientSocket.send("2")
        print("done")


if __name__ == '__main__':
    main()
