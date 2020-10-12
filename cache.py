import cache_set
from random import randint

class Cache:
  def __init__(self, id):
    self.set_0 = cache_set.Set(id, 0)
    self.set_1 = cache_set.Set(id, 1)

  def read(self, address):
    cache_set = address%2
    line_0 = None
    line_1 = None
    if(cache_set==0):
      line_0 = self.set_0.block_0
      line_1 = self.set_0.block_1
    elif(cache_set==1):
      line_0 = self.set_1.block_0
      line_1 = self.set_1.block_1

    if(address==line_0.tag):
      return line_0
    elif(address==line_1.tag):
      return line_1
    else:
      return None

  def write(self, address, data):
    cache_set = address%2
    line_0 = None
    line_1 = None
    if(cache_set==0):
      line_0 = self.set_0.block_0
      line_1 = self.set_0.block_1

      if(line_0.tag==address or line_0.tag==None):
        self.set_0.block_0.tag = address
        self.set_0.block_0.data = data
      elif(line_1.tag==address or line_1.tag==None):
        self.set_0.block_1.tag = address
        self.set_0.block_1.data = data
      else:
        line = bool(randint(0, 1))
        if(line):
          self.set_0.block_1.tag = address
          self.set_0.block_1.data = data
        else:
          self.set_0.block_0.tag = address
          self.set_0.block_0.data = data

    elif(cache_set==1):
      line_0 = self.set_1.block_0
      line_1 = self.set_1.block_1

      if(line_0.tag==address or line_0.tag==None):
        self.set_1.block_0.tag = address
        self.set_1.block_0.data = data
      elif(line_1.tag==address or line_1.tag==None):
        self.set_1.block_1.tag = address
        self.set_1.block_1.data = data
      else:
        line = bool(randint(0, 1))
        if(line):
          self.set_1.block_1.tag = address
          self.set_1.block_1.data = data
        else:
          self.set_1.block_0.tag = address
          self.set_1.block_0.data = data


  def set_state(self, address, state):
    cache_set = address%2
    line_0 = None
    line_1 = None
    if(cache_set==0):
      line_0 = self.set_0.block_0
      line_1 = self.set_0.block_1

      if(line_0.tag==address or line_0.tag==None):
        self.set_0.block_0.state = state
      elif(line_1.tag==address or line_1.tag==None):
        self.set_0.block_1.state = state
      else:
        line = bool(randint(0, 1))
        if(line):
          self.set_0.block_1.state = state
        else:
          self.set_0.block_0.state = state

    elif(cache_set==1):
      line_0 = self.set_1.block_0
      line_1 = self.set_1.block_1

      if(line_0.tag==address or line_0.tag==None):
        self.set_1.block_0.state = state
      elif(line_1.tag==address or line_1.tag==None):
        self.set_1.block_1.state = state
      else:
        line = bool(randint(0, 1))
        if(line):
          self.set_1.block_1.state = state
        else:
          self.set_1.block_0.state = state
