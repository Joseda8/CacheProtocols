from queue import Queue 
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

import cache
import instruction
import util
import multiprocessing

NUM_PROC = 2

class Processor:
    def __init__(self, id):
        self.id = multiprocessing.Value('i', id)
        self.is_cache_busy = multiprocessing.Value('i', False)
        self.cache = cache.Cache()
        self.inst = []
        self.is_inst_busy = multiprocessing.Value('i', False)
        self.inst_exe = None

    def get_inst_exe(self):    
        while(True):
            if(not self.is_inst_busy.value):
                self.is_inst_busy.value = True
                data = self.inst_exe
                self.is_inst_busy.value = False
                return data

    def set_inst(self, inst):    
        while(True):
            if(not self.is_inst_busy.value):
                self.is_inst_busy.value = True
                self.inst_exe = inst
                self.is_inst_busy.value = False
                break

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
        clk = 0
        while(True):
            new_msg = self.get_msg(msg)
            status = new_msg["status"]
            ans = new_msg["ans"]
            if(status and new_msg["req"].type == "WRITE"):
                if(ans not in proc):
                    proc.append(ans)
                if(len(proc)==NUM_PROC-1):
                    break
            clk += 1
            if(clk==10000):
                break
        self.clear_msg(msg)
    
    def print_inst(self):
        a = []
        for ins in self.inst:
            a.append(ins.type)
        print(f"Procesador {self.id.value}", a)

    def new_inst(self):
        inst_rand = util.get_inst()
        for inst in inst_rand:
            if(inst == 0):
                self.inst.append(instruction.Instruction(self.id.value, "CALC", None))
            elif(inst == 1):
                addr = util.get_randint(0, 2)
                self.inst.append(instruction.Instruction(self.id.value, "READ", [addr]))
            elif(inst == 2):
                addr = util.get_randint(0, 2)
                data = util.get_randint(0, 65535)
                self.inst.append(instruction.Instruction(self.id.value, "WRITE", [addr, data]))

    def inst_run(self, clk, bus, msg):
        inst_to_run = self.inst[-1]
        self.set_inst(self.inst[-1])
        inst_type = inst_to_run.type
        start_clk = clk.value
        if(inst_type=="READ" and not bus.get_busy()):
            data = self.read_cache(inst_to_run.addr)
            if(data is not None):
                print(f"CYCLE {start_clk}, PROC: {self.id.value}, READ MY CACHE:", inst_to_run.addr, data.data)
                self.inst.pop()
            else:
                bus.set_inst(inst_to_run)
                self.insert_msg(msg, inst_to_run, None, None)
                data = self.wait_ans(msg)
                if(data["ans"] is not None):
                    data = data["ans"]
                    print(f"CYCLE {start_clk}, PROC: {self.id.value}, READ CACHE:", inst_to_run.addr, data)
                    self.write_cache(inst_to_run.addr, data)
                    self.set_state(inst_to_run.addr, "S")
                else:
                    data = bus.read_mem(inst_to_run.addr)
                    print(f"CYCLE {start_clk}, PROC: {self.id.value}, READ MEM:", inst_to_run.addr, data)
                    while(clk.value-start_clk<=1):
                        pass
                    self.write_cache(inst_to_run.addr, data)
                    self.set_state(inst_to_run.addr, "E")
                self.inst.pop()
            bus.set_inst(None)
            bus.set_busy(False)
        elif(inst_type=="WRITE" and not bus.get_busy()):
            bus.set_inst(inst_to_run)
            bus.write_mem(inst_to_run.addr, inst_to_run.data)
            data = self.read_cache(inst_to_run.addr)
            if(data is not None):
                self.insert_msg(msg, inst_to_run, None, None)
                self.wait_write(msg)
                self.write_cache(inst_to_run.addr, inst_to_run.data)
            else:
                read_inst = instruction.Instruction(self.id.value, "READ", [inst_to_run.addr])
                self.insert_msg(msg, read_inst, None, None)
                data = self.wait_ans(msg)
                if(data["ans"] is not None):
                    self.insert_msg(msg, inst_to_run, None, None)
                    self.wait_write(msg)
                    self.write_cache(inst_to_run.addr, inst_to_run.data)
                    self.set_state(inst_to_run.addr, "S")
                else:
                    self.insert_msg(msg, inst_to_run, None, None)
                    self.wait_write(msg)
                    self.write_cache(inst_to_run.addr, inst_to_run.data)                    
                    self.set_state(inst_to_run.addr, "E")

            print(f"CYCLE {start_clk}, PROC: {self.id.value}, WRITE", inst_to_run.addr, inst_to_run.data)
            while(clk.value-start_clk<=2):
                pass
            self.inst.pop()
            bus.set_inst(None)
            bus.set_busy(False)
        elif(inst_type=="CALC"):
            print(f"CYCLE {clk.value}, PROC: {self.id.value}, CALC")
            self.inst.pop()

    def cpu_run(self, clk, bus, msg):
        clk_bef = 0 
        while(True):
            new_clk = clk.value
            if(clk_bef != new_clk):
                """
                try:
                    x_lines = self.get_lines()
                    print(f"\nCYCLE {new_clk}, PROC: {self.id.value}, STATE: {x_lines[0].state} {x_lines[1].state} \nDATA: {x_lines[0].tag}-{x_lines[0].data} {x_lines[1].tag}-{x_lines[1].data}\n")
                    pass
                except:
                    print(f"CYCLE {new_clk}, PROC: {self.id.value}, STATE: None")
                    pass
                """
                if(len(self.inst)==0):
                    self.new_inst()
                    #self.print_inst()
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
                if(inst.proc_id != self.id.value):
                    if(new_msg["req"].type=="READ"):
                        line = self.read_cache(inst.addr)
                        if(line is None):
                            self.insert_msg(msg, inst, self.id.value, False)
                        elif(line.state=="E" or line.state=="O"):
                            self.set_state(line.tag, "O")
                            self.insert_msg(msg, inst, line.data, True)
                        else:
                            self.set_state(line.tag, "O")
                            self.insert_msg(msg, inst, line.data, True)
                    elif(new_msg["req"].type=="WRITE"):
                        if(self.read_cache(inst.addr) is not None):
                            self.write_cache(inst.addr, inst.data)
                        self.insert_msg(msg, inst, self.id.value, True)

            clk_bef = new_clk
            
            