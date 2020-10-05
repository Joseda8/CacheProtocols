import cache
import instruction
import util

class Processor:
    def __init__(self, id):
        self.id = id
        self.cache = cache.Cache()
        self.inst = []

    def get_data(self, address):
        return self.cache.set_0.block_0.data

    def new_inst(self):
        inst_rand = util.get_inst()
        for inst in inst_rand:
            if(inst == 0):
                self.inst.append(instruction.Instruction(self.id, "CALC", None))
            elif(inst == 1):
                self.inst.append(instruction.Instruction(self.id, "READ", [8]))
            elif(inst == 2):
                self.inst.append(instruction.Instruction(self.id, "WRITE", [5, 7]))

    def cpu_run(self, clk, bus):
        clk_bef = 0 

        while(True):
            new_clk = clk.value
            if(clk_bef != new_clk):
                if(len(self.inst)==0):
                    self.new_inst()
                else:
                    inst_to_run = self.inst.pop()

            clk_bef = new_clk
            