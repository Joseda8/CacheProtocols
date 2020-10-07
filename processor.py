import cache
import instruction
import util
import multiprocessing

class Processor:
    def __init__(self, id):
        self.id = id
        self.is_cache_busy = multiprocessing.Value('i', False)
        self.cache = cache.Cache()
        self.inst = []
    
    def print_inst(self):
        a = []
        for ins in self.inst:
            a.append(ins.type)
        print(f"Procesador {self.id}", a)

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
                bus.set_inst(inst_to_run)
                data = bus.read_mem(inst_to_run.addr)
                print(f"READ {self.id}, CYCLE {start_clk}:", data)
                while(clk.value-start_clk<=1):
                    pass
                self.inst.pop()
                bus.set_inst(None)
                bus.set_busy(False)
        elif(inst_type=="WRITE"):
            if(not bus.get_busy()):
                bus.set_inst(inst_to_run)
                bus.write_mem(inst_to_run.addr, inst_to_run.data)
                print(f"WRITE {self.id}, CYCLE {start_clk}")
                while(clk.value-start_clk<=2):
                    pass
                self.inst.pop()
                bus.set_inst(None)
                bus.set_busy(False)
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
                    #self.print_inst()
                else:
                    self.inst_run(clk, bus)

            clk_bef = new_clk

    def snoopy(self):
        pass
            
            