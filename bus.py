import memory 

class Bus:
    def __init__(self):
        self.memory = memory.Memory()
        self.busy = False
        self.inst = None

    def get_mem(self):
        mem_busy = self.memory.busy 
        if(not mem_busy):
            return self.memory
        else:
            return False