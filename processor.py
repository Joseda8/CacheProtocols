from queue import Queue 

import cache
import instruction
import util
import multiprocessing

NUM_PROC = 2

class Processor:
    def __init__(self, id):
        self.id = id
        self.is_cache_busy = multiprocessing.Value('i', False)
        self.cache = cache.Cache()
        self.inst = []

    def read_cache(self, addr):    
        while(True):
            if(not self.is_cache_busy.value):
                self.is_cache_busy.value = True
                data = self.cache.read(addr)
                self.is_cache_busy.value = False
                return data

    def write_cache(self, addr, data):
        while(True):
            if(not self.is_cache_busy.value):
                self.is_cache_busy.value = True
                self.cache.write(addr, data)
                self.is_cache_busy.value = False
                return data

    def clear_msg(self, msg):
        while(not msg.empty()):
            msg.get()
            msg.task_done()

    def insert_msg(self, msg, req, ans, status):
        self.clear_msg(msg)
        msg.put({"req": req, "ans": ans, "status": status})

    def get_msg(self, msg):
        new_msg = msg.get()
        msg.task_done()
        self.insert_msg(msg, new_msg["req"], new_msg["ans"], new_msg["status"])
        return new_msg

    def wait_ans(self, msg):
        proc = []
        while(True):
            new_msg = self.get_msg(msg)
            status = new_msg["status"]
            ans = new_msg["ans"]
            if(status):
                break
            elif(status==False):
                if(ans not in proc):
                    proc.append(ans)
            if(len(proc)==NUM_PROC-1):
                new_msg["ans"] = None
                break
        self.clear_msg(msg)
        return new_msg
    
    def wait_write(self, msg):
        proc = []
        while(True):
            new_msg = self.get_msg(msg)
            status = new_msg["status"]
            ans = new_msg["ans"]
            if(status):
                if(ans not in proc):
                    proc.append(ans)
                if(len(proc)==NUM_PROC-1):
                    break
        self.clear_msg(msg)
    
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
                addr = util.get_randint(0, 15)
                self.inst.append(instruction.Instruction(self.id, "READ", [addr]))
            elif(inst == 2):
                addr = util.get_randint(0, 15)
                data = util.get_randint(0, 65535)
                self.inst.append(instruction.Instruction(self.id, "WRITE", [addr, data]))
        self.inst = [instruction.Instruction(self.id, "READ", [9]), instruction.Instruction(self.id, "WRITE", [8, 12]), instruction.Instruction(self.id, "WRITE", [9, 200]), instruction.Instruction(self.id, "READ", [9]), instruction.Instruction(self.id, "READ", [9])]

    def inst_run(self, clk, bus, msg):
        inst_to_run = self.inst[-1]
        inst_type = inst_to_run.type
        start_clk = clk.value
        if(inst_type=="READ"):
            data = self.read_cache(inst_to_run.addr)
            if(data is not None):
                print(f"CYCLE {start_clk}, PROC: {self.id}, READ MY CACHE:", inst_to_run.addr, data.data)
                self.write_cache(inst_to_run.addr, data.data)
                self.inst.pop()
            elif(not bus.get_busy()):
                bus.set_inst(inst_to_run)
                self.insert_msg(msg, inst_to_run, None, None)
                data = self.wait_ans(msg)
                if(data["ans"] is not None):
                    data = data["ans"]
                    print(f"CYCLE {start_clk}, PROC: {self.id}, READ CACHE:", inst_to_run.addr, data)
                else:
                    data = bus.read_mem(inst_to_run.addr)
                    print(f"CYCLE {start_clk}, PROC: {self.id}, READ MEM:", inst_to_run.addr, data)
                    while(clk.value-start_clk<=1):
                        pass
                self.write_cache(inst_to_run.addr, data)
                self.inst.pop()
                bus.set_inst(None)
                bus.set_busy(False)
        elif(inst_type=="WRITE"):
            if(not bus.get_busy()):
                bus.set_inst(inst_to_run)
                bus.write_mem(inst_to_run.addr, inst_to_run.data)
                print(f"CYCLE {start_clk}, PROC: {self.id}, WRITE", inst_to_run.addr, inst_to_run.data)
                while(clk.value-start_clk<=2):
                    pass
                self.write_cache(inst_to_run.addr, inst_to_run.data)
                self.insert_msg(msg, inst_to_run, None, None)
                self.wait_write(msg)
                self.inst.pop()
                bus.set_inst(None)
                bus.set_busy(False)
        elif(inst_type=="CALC"):
            print(f"CYCLE {clk.value}, PROC: {self.id}, CALC")
            self.inst.pop()

    def cpu_run(self, clk, bus, msg):
        clk_bef = 0 
        while(True):
            new_clk = clk.value
            if(clk_bef != new_clk):
                if(len(self.inst)==0):
                    self.new_inst()
                    self.print_inst()
                else:
                    self.inst_run(clk, bus, msg)

            clk_bef = new_clk

    def snoopy(self, clk, bus, msg):
        clk_bef = 0 
        while(True):
            new_clk = clk.value
            if(clk_bef != new_clk):
                new_msg = self.get_msg(msg)
                inst = new_msg["req"]
                if(inst.proc_id != self.id):
                    if(new_msg["req"].type=="READ"):
                        line = self.read_cache(inst.addr)
                        if(line is None):
                            self.insert_msg(msg, inst, self.id, False)
                        else:
                            self.insert_msg(msg, inst, line.data, True)
                    elif(new_msg["req"].type=="WRITE"):
                        self.write_cache(inst.addr, inst.data)
                        self.insert_msg(msg, inst, self.id, True)

            clk_bef = new_clk
            
            