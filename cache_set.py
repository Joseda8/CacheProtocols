import cache_line

class Set:
  def __init__(self):
    self.block_0 = cache_line.Block(0)
    self.block_1 = cache_line.Block(1)
