class Instruction:
    def __init__(self, proc_id, inst, data):
        self.proc_id = proc_id
        self.type = inst
        if(inst=="READ" or inst=="READ_W"):
            self.addr = data[0]
        elif(inst=="WRITE"):
            self.addr = data[0]
            self.data = data[1]

    def __str__(self):
        if(self.type=="CALC"):
            return "CALC"
        elif(self.type=="READ"):
            return f"R: {bin(self.addr)[2:]}"
        else:
            return f"W: {bin(self.addr)[2:]}, {hex(self.data)}"