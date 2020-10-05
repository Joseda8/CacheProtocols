import cache

class Processor:
    def __init__(self, id):
        self.id = id
        self.cache = cache.Cache()
        self.inst = []

    def get_data(self, address):
        return self.cache.set_0.block_0.data