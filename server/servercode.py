##
# Class for managing clients connected to the game

import socket
import threading
import time
from PyQt5.QtCore import pyqtSignal as signal, QObject
from server.client import Client


##
#  Basic class for accepting clients and passing along their information
class Server(QObject):

    address = None
    port = 5000

    newCliSig = signal(int)

    def __init__(self, *args, **kargs):
      super().__init__(*args, **kargs)
      self.socket = socket.socket()
      self.address = socket.gethostbyname(socket.gethostname())
      self.socket.bind((self.address, self.port))
      self.socket.listen(5)
      self.listening = False
      self.clients = []
      acceptThread = threading.Thread(target=self.acceptClient, daemon=True)
      acceptThread.start()

    ##
    # Runs an infinite loop in a separate thread to accept all incoming clients
    def acceptClient(self):
      self.listening = True
      print("Now Listening to clients on IP: {} port: {}".format(self.address, self.port))
      while self.listening:
        cliSock, cliAddr = self.socket.accept()
        print("Client {} has connected to the server.".format(cliAddr[0]))
        self.clients.append(Client(cliSock))
        self.newCliSig.emit(len(self.clients))

if __name__ == "__main__":
  server = Server()
  client = None
  def onNewCliSig():
    pass
  server.newCliSig.connect(onNewCliSig)
  while len(server.clients) == 0:
    time.sleep(1)
  client = server.clients[0]
  def echo():
    while True:
      try:
        cliData = client.read()
      except socket.error:
        break
      if cliData != "":
        client.write(cliData)
  echoThread = threading.Thread(target=echo, name="Echo Thread", daemon=True)
  echoThread.start()
  while True:
    data = input()
    if data == "stop":
      break
    if data == "readbuff":
      print("readbuffer:", client.readBuff)
    if data == "writebuff":
      print("writebuffer:", client.writeBuff)
