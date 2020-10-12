import cache_line

class Set:
  def __init__(self, id, set):
    self.block_0 = cache_line.Block(id, set, 0)
    self.block_1 = cache_line.Block(id, set, 1)
