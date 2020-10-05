import memory 

class Bus:
    def __init__(self):
        self.memory = memory.Memory()
        self.busy = False
        self.inst = None

    def get_busy(self):
        return self.busy
    
    def set_busy(self, status):
        self.busy = status
        return True

    def get_inst(self):
        return self.inst
    
    def set_inst(self, inst):
        self.inst = inst
        return True

    def read_mem(self, address):
        if(not self.memory.busy):
            self.memory.busy = True
            return self.memory.get_data(address)
        else:
            return False
            
    def write_mem(self, address, data):
        if(not self.memory.busy):
            self.memory.busy = True
            self.memory.set_data(address, data)
            return True
        else:
            return False

    def leave_mem(self):
        self.memory.busy = False
        return True
