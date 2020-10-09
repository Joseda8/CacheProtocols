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

    def get_lines(self):
        while(True):
            if(not self.is_cache_busy.value):
                self.is_cache_busy.value = True
                data = (self.cache.set_0.block_0, self.cache.set_0.block_1, self.cache.set_1.block_0, self.cache.set_1.block_1)
                self.is_cache_busy.value = False
                return data

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
                break

    def set_state(self, addr, state):
        while(True):
            if(not self.is_cache_busy.value):
                self.is_cache_busy.value = True
                self.cache.set_state(addr, state)
                self.is_cache_busy.value = False
                break

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
                addr = util.get_randint(0, 1)
                self.inst.append(instruction.Instruction(self.id, "READ", [addr]))
            elif(inst == 2):
                addr = util.get_randint(0, 4)
                data = util.get_randint(0, 65535)
                self.inst.append(instruction.Instruction(self.id, "WRITE", [addr, data]))

        new_inst = []
        if(self.id==1):
            new_inst.append(instruction.Instruction(self.id, "READ", [0]))
            new_inst.append(instruction.Instruction(self.id, "WRITE", [0, 8]))
            new_inst.append(instruction.Instruction(self.id, "WRITE", [2, 8]))
            new_inst.append(instruction.Instruction(self.id, "WRITE", [4, 8]))
            new_inst.append(instruction.Instruction(self.id, "WRITE", [6, 8]))
            new_inst.append(instruction.Instruction(self.id, "READ", [0]))
        elif(self.id==2):
            new_inst.append(instruction.Instruction(self.id, "READ", [0]))
            new_inst.append(instruction.Instruction(self.id, "READ", [0]))

        self.inst = new_inst
            

    def inst_run(self, clk, bus, msg):
        inst_to_run = self.inst[-1]
        inst_type = inst_to_run.type
        start_clk = clk.value
        if(inst_type=="READ"):
            data = self.read_cache(inst_to_run.addr)
            if(data is not None and (not bus.get_busy()) ):
                print(f"CYCLE {start_clk}, PROC: {self.id}, READ MY CACHE:", inst_to_run.addr, data.data)
                self.write_cache(inst_to_run.addr, data.data)
                self.inst.pop()
                bus.set_inst(None)
                bus.set_busy(False)
            elif(not bus.get_busy()):
                bus.set_inst(inst_to_run)
                self.insert_msg(msg, inst_to_run, None, None)
                data = self.wait_ans(msg)
                if(data["ans"] is not None):
                    data = data["ans"]
                    print(f"CYCLE {start_clk}, PROC: {self.id}, READ CACHE:", inst_to_run.addr, data)
                    self.set_state(inst_to_run.addr, "S")
                    self.write_cache(inst_to_run.addr, data)
                else:
                    data = bus.read_mem(inst_to_run.addr)
                    print(f"CYCLE {start_clk}, PROC: {self.id}, READ MEM:", inst_to_run.addr, data)
                    self.write_cache(inst_to_run.addr, data)
                    self.set_state(inst_to_run.addr, "E")
                    while(clk.value-start_clk<=1):
                        pass
                self.inst.pop()
                bus.set_inst(None)
                bus.set_busy(False)
        elif(inst_type=="WRITE"):
            if(not bus.get_busy()):
                bus.set_inst(inst_to_run)
                bus.write_mem(inst_to_run.addr, inst_to_run.data)
                print(f"CYCLE {start_clk}, PROC: {self.id}, WRITE", inst_to_run.addr, inst_to_run.data)
                line = self.read_cache(inst_to_run.addr)
                self.write_cache(inst_to_run.addr, inst_to_run.data)
                if(line is None):
                    read_inst = instruction.Instruction(self.id, "READ", [inst_to_run.addr])
                    self.insert_msg(msg, read_inst, None, None)
                    print("ENTER")
                    data = self.wait_ans(msg)
                    print("OUT", data)
                    if(data["ans"] is None):
                        self.set_state(inst_to_run.addr, "E")
                    else:
                        self.set_state(inst_to_run.addr, "S")
                self.insert_msg(msg, inst_to_run, None, None)
                self.wait_write(msg)
                while(clk.value-start_clk<=2):
                    pass
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
                try:
                    x_lines = self.get_lines()
                    print(f"\nCYCLE {new_clk}, PROC: {self.id}, STATE: {x_lines[0].state} {x_lines[1].state} \nDATA: {x_lines[0].tag}-{x_lines[0].data} {x_lines[1].tag}-{x_lines[1].data}\n")
                    pass
                except:
                    print(f"CYCLE {new_clk}, PROC: {self.id}, STATE: None")
                    pass
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
                        elif(line.state == "O"):
                            self.insert_msg(msg, inst, line.data, True)
                        else:
                            print("OWNED", self.id, inst.addr, inst.proc_id)
                            self.set_state(inst.addr, "O")
                            self.insert_msg(msg, inst, line.data, True)
                    elif(new_msg["req"].type=="WRITE"):
                        if(self.read_cache(inst.addr) is not None):
                            self.write_cache(inst.addr, inst.data)
                        else:
                            lines = self.get_lines()
                            for line in lines:
                                if(line.tag is not None):
                                    read_inst = instruction.Instruction(self.id, "READ", [line.tag])
                                    self.insert_msg(msg, read_inst, None, None)
                                    data = self.wait_ans(msg)
                                    print("CLEANING", self.id, data["ans"], data["req"].proc_id, data["req"].addr)
                                    if(data["ans"] is None):
                                        self.set_state(line.tag, "E")

                        self.insert_msg(msg, inst, self.id, True)

            clk_bef = new_clk
            
            