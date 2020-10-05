class Memory:
    def __init__(self):
        self.memory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_data(self, address):
        print(self.memory[address])
        return self.memory[address]

    def set_data(self, address, data):
        self.memory[address] = data