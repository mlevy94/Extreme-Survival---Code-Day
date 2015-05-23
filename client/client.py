##
# Basic TCP client to communicate with the game server

class Client():

  def __init__(self, socket=None):
    self.socket = socket

