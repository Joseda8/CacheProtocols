class Block:
  def __init__(self, proc, set, id):
    self.id = id
    self.tag = None 
    self.state = None
    self.data = 0
    self.name = str(proc) + str(set) + str(id)