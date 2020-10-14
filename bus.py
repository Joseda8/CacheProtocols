import memory 
import multiprocessing

class Bus:
    def __init__(self):
        self.memory = memory.Memory()
        self.busy = multiprocessing.Value('i', False)
        self.is_inst_busy = multiprocessing.Value('i', False)
        self.inst = None

    def get_busy(self):
        is_busy = True
        if(not self.busy.value):
            self.busy.value = True
            is_busy = False
        return is_busy
    
    def set_busy(self, status):
        self.busy.value = status
        return True

    def get_inst(self):    
        data = self.inst
        return data

    def set_inst(self, new_inst):    
        self.inst = new_inst

    def read_mem(self, address):
        return self.memory.get_data(address)

    def write_mem(self, address, data):
        self.memory.set_data(address, data)
        return True

    def get_mem(self):
        mem = self.memory.get_mem()
        return mem
