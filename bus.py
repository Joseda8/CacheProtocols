import memory 

class Bus:
    def __init__(self):
        self.memory = memory.Memory()
        self.busy = False
        self.inst = None

    def get_busy(self):
        is_busy = True
        if(not self.busy):
            self.busy = True
            is_busy = False
        return is_busy
    
    def set_busy(self, status):
        self.busy = status
        return True

    def get_inst(self):
        return self.inst
    
    def set_inst(self, inst):
        self.inst = inst
        return True

    def read_mem(self, address):
        return self.memory.get_data(address)

    def write_mem(self, address, data):
        self.memory.set_data(address, data)
        return True
