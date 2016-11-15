import socket


# Class for Server
class Server(object):

  backlog = 5
  client = None

  def __init__(self, host, port):
    self.socket = socket.socket()
    self.socket.bind((host, port))
    self.socket.listen(self.backlog)

  def __del__(self):
    self.close()

  def accept(self):
    # if a client is already connected, disconnect it
    if self.client:
      print('3')  
      self.client.close()
    self.client, self.client_addr = self.socket.accept()
    return self

  def send(self, data):
    if not self.client:
      raise Exception('Cannot send data, no client is connected')
    self.client.send(data)
    return self

  def recv(self):
    if not self.client:
      raise Exception('Cannot receive data, no client is connected')
    return self.client.recv(30000)

  def close(self):
    if self.client:
      self.client.close()
      self.client = None
    if self.socket:
      self.socket.close()
      self.socket = None


      
#Class for Client 
class Client(object):

  socket = None

  def __del__(self):
    self.close()

  def connect(self, host, port):
    self.socket = socket.socket()
    self.socket.connect((host, port))
    return self

  def send(self, data):
    if not self.socket:
      raise Exception('You have to connect first before sending data')
    self.socket.send(data)
    return self

  def recv(self):
    if not self.socket:
      raise Exception('You have to connect first before receiving data')
    return self.socket.recv(30000)

  def recv_and_close(self):
    data = self.recv()
    self.close()
    return data

  def close(self):
    if self.socket:
      self.socket.close()
      self.socket = None


