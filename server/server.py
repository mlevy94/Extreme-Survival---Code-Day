##
# Class for managing clients connected to the game

from client.client import Client
from PyQt5.QtCore import pyqtSignal as signal
import socket
import threading

##
#  Basic class for accepting clients and passing along their information
class Server():

    address = None
    port = 5000

    newCliSig = signal(Client)

    def __init__(self):
      self.socket = socket.socket()
      self.address = socket.gethostbyname(socket.gethostname())
      self.socket.bind(self.address)
      self.socket.listen(5)
      self.listening = False
      acceptThread = threading.Thread(target=self.acceptClient, daemon=True)
      acceptThread.start()

    ##
    # Runs an infinite loop in a separate thread to accept all incoming clients
    def acceptClient(self):
      self.listening = True
      print("Now Listening to clients on IP: {} port: {}".format(self.address, self.port))
      while not self.listening:
        cliSock, cliAddr = self.socket.accept()
        print("Client {} has connected to the server.".format(cliAddr))
        self.newCliSig.emit(Client(cliSock))
