class Memory:
    def __init__(self):
        self.memory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_data(self, address):
        return self.memory[address]

    def set_data(self, address, data):
        self.memory[address] = data

    def get_mem(self):
        mem = self.memory
        return mem


