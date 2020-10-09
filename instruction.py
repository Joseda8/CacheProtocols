class Instruction:
    def __init__(self, proc_id, inst, data):
        self.proc_id = proc_id
        self.type = inst
        if(inst=="READ" or inst=="READ_W"):
            self.addr = data[0]
        elif(inst=="WRITE"):
            self.addr = data[0]
            self.data = data[1]
