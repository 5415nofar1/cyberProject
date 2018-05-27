import socket

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)


def first_connect_message():
    pass

    def func1():
        print 1
        return 1

    def func2():
        print 2
        return 2

    action_dict = {
        0: first_connect_message,
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
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    # Listen for incoming datagrams
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)

        response = manipulate_message(message)

        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)


if __name__ == '__main__':
    main()
