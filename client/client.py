##
# client side client class

from server.client import Client
import socket
import threading

def main(address, port):
    cliSock = socket.socket()
    cliSock.settimeout(1)
    connected = False
    while not connected:
        try:
            cliSock.connect((address, port))
            print("Now connected to game server at {} port {}".format(address, port))
            connected = True
        except socket.timeout:
            print("Could not connect to server. Please enter address again")
            address = input()
    client = Client(cliSock)
    def printToScreen():
        while True:
            try:
                readData = client.read()
            except socket.error:
                break
            if readData != "":
                print(readData)
    readThread = threading.Thread(target=printToScreen, name = "Read Thread", daemon=True)
    readThread.start()
    while True:
        writeData = input()
        if writeData in ["quit", "exit", "logout"]:
            print("Thanks for playing!")
            break
        elif writeData in ['reconnect']:
            client.close()
            print('Reconnecting')
            main(address, port)
            return
        elif writeData in ['restart']:
            client.close()
            print('Restarting')
            run()
            return
        else:
            client.write(writeData)
    client.close()
    print("Disconnected from server {}".format(address))

def run():
    print("Welcome to Extreme Survival - Code Day")
    print("Please enter the IP of the server you wish to connect to.")
    address = input()
    port = int(input("Port to connect to\n"))
    main(address, port)


if __name__ == "__main__":
    run()