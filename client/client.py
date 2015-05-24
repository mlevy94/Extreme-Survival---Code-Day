##
# client side client class

from server.client import Client
import socket
import threading

def printToScreen():
  while not exitGame:
    readData = client.read()
    if readData != "":
      print(readData)


if __name__ == "__main__":
  print("Welcome to Extreme Survival - Code Day")
  print("Please enter the IP of the server you wish to connect to.")
  port = 5000
  address = input()
  cliSock = socket.socket()
  cliSock.settimeout(0)
  connected = False
  while not connected:
    try:
      cliSock.connect((address, port))
    except socket.timeout:
      print("Could not connect to server. Please enter address again")
      address = input()
  client = Client(cliSock)
  readThread = threading.Thread(target=printToScreen, name = "Read Thread", daemon=True)
  exitGame = False
  while not exitGame:
    writeData = input()
    if writeData in ["quit", "exit", "logout"]:
      exitGame = True
    else:
      client.write(writeData)
  client.close()
  readThread.join()