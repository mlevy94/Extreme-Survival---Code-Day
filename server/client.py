##
# Basic TCP client to communicate with the game server

import threading


class Client():

  def __init__(self, socket=None):
    self.socket = socket
    self.readBuff = ""
    self.writeBuff = ""
    self.readSock = False
    self.writeSock = False
    self.writeThread = threading.Thread(target=self._write, name="Write Thread")
    self.readThread = threading.Thread(target=self._read, name="Read Thread")
    self.writeThread.start()
    self.readThread.start()

  def read(self):
    data = self.readBuff
    self.readBuff = ""
    return data

  def write(self, data):
    if isinstance(data, str):
      self.writeBuff += data
    else:
      raise Exception("write received a bad data type")


  def _read(self):
    # TODO add signal so this doesn't keep reading when client disconnects
    self.readSock = True
    while self.readSock:
      data = self.socket.recv(4096)
      if data != b'':
        self.readBuff += data.encode()

  def _write(self):
    self.writeSock = True
    while self.writeSock:
      if self.writeBuff != "":
        data = self.writeBuff
        self.socket.sendAll(data.encode())
        self.writeBuff = self.writeBuff.replace(data, "")
