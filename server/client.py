##
# Basic TCP client to communicate with the game server

from PyQt5.QtCore import pyqtSignal as signal, QObject
import threading
import socket


class Client(QObject):

  def __init__(self, cliSocket=None, *args, **kargs):
    super().__init__(*args, **kargs)
    self.clientDisconnected = signal()
    self.socket = cliSocket
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
    self.readSock = True
    while self.readSock:
      try:
        data = self.socket.recv(4096)
      except socket.timeout:
        pass
      except socket.error:
        print("quitting")
        self._close()
        break
      else:
        if data != b'':
          self.readBuff += data.decode()


  def _write(self):
    self.writeSock = True
    while self.writeSock:
      if self.writeBuff != "":
        data = self.writeBuff
        self.socket.sendall(data.encode())
        self.writeBuff = self.writeBuff.replace(data, "")

  def _close(self):
    self.writeSock = False
    self.writeThread.join()
    try:
      pass
      #self.readThread.join()
    except RuntimeError:
      pass # close called by read thread losing connection
    try:
      self.clientDisconnected.emit()
    except AttributeError:
      pass # no one connected to this signal

  def close(self):
    self.socket.shutdown(socket.SHUT_RDWR)
    self.socket.close()
    self._close()



