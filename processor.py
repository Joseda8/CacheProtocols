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
                self.inst.append(instruction.Instruction(self.id, "WRITE", [8, 7]))

    def inst_run(self, clk, bus):
        inst_to_run = self.inst[-1]
        inst_type = inst_to_run.type
        start_clk = clk.value
        if(inst_type=="READ"):
            if(not bus.get_busy()):
                bus.set_busy(True)
                data = bus.read_mem(inst_to_run.addr)
                bus.set_busy(False)
                if(data != False):
                    print(f"READ {self.id}, CYCLE {start_clk}:", data)
                    while(clk.value-start_clk<=2):
                        pass
                    self.inst.pop()
                    bus.leave_mem()
        elif(inst_type=="WRITE"):
            if(not bus.get_busy()):
                bus.set_busy(True)
                result = bus.write_mem(inst_to_run.addr, inst_to_run.data)
                bus.set_busy(False)
                if(result):
                    print(f"WRITE {self.id}, CYCLE {start_clk}")
                    while(clk.value-start_clk<=3):
                        pass
                    self.inst.pop()
                    bus.leave_mem()
        elif(inst_type=="CALC"):
            print(f"CALC {self.id}, CYCLE {clk.value}")
            self.inst.pop()
        

    def cpu_run(self, clk, bus):
        clk_bef = 0 

        while(True):
            new_clk = clk.value
            if(clk_bef != new_clk):
                if(len(self.inst)==0):
                    self.new_inst()
                    a = []
                    for ins in self.inst:
                        a.append(ins.type)
                    print(f"Procesador {self.id}", a)
                else:
                    self.inst_run(clk, bus)
                #print(bus.get_mem().get_data(8))
                #print(bus.get_busy())

            clk_bef = new_clk
            
            