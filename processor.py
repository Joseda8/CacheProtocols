from queue import Queue 
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

import cache
import instruction
import util
import multiprocessing

NUM_PROC = 4

class Processor:
    def __init__(self, id):
        self.id = multiprocessing.Value('i', id)
        self.is_cache_busy = multiprocessing.Value('i', False)
        self.cache = cache.Cache(id)
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
        new_inst = []
        if(self.id.value==1):
            new_inst.append(instruction.Instruction(self.id.value, "READ", [0]))
            new_inst.append(instruction.Instruction(self.id.value, "WRITE", [0, 8]))
            new_inst.append(instruction.Instruction(self.id.value, "WRITE", [2, 8]))
            new_inst.append(instruction.Instruction(self.id.value, "WRITE", [4, 8]))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
            new_inst.append(instruction.Instruction(self.id.value, "READ", [0]))
        elif(self.id.value==2):
            new_inst.append(instruction.Instruction(self.id.value, "READ", [0]))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
        elif(self.id.value==3):
            new_inst.append(instruction.Instruction(self.id.value, "READ", [0]))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
            new_inst.append(instruction.Instruction(self.id.value, "READ", [1]))
        elif(self.id.value==4):
            new_inst.append(instruction.Instruction(self.id.value, "READ", [0]))
            new_inst.append(instruction.Instruction(self.id.value, "WRITE", [1, 8]))
            new_inst.append(instruction.Instruction(self.id.value, "WRITE", [2, 8]))
            new_inst.append(instruction.Instruction(self.id.value, "WRITE", [4, 8]))
            new_inst.append(instruction.Instruction(self.id.value, "CALC", None))
            new_inst.append(instruction.Instruction(self.id.value, "READ", [0]))

        self.inst = new_inst

    def search_data(self, processors, addr):
        data = None
        for proc in processors:
            if(self.id.value != proc.id.value):
                data = proc.read_cache(addr)
                if(data is not None):
                    data = data
                    exclusive = True
                    test_data = None
                    for proc_2 in processors:
                        if(proc.id.value != proc_2.id.value):
                            test_data = proc_2.read_cache(addr)
                            if(test_data is not None):
                                exclusive = False
                    if(exclusive):
                        proc.set_state(addr, "O")
                    break
        return data


    def search_shared_data(self, processors, proc_id, addr):
        result = []
        for proc in processors:
            if(proc.id.value != self.id.value != proc_id):
                data = proc.read_cache(addr)
                if(data is not None):
                    result.append(proc.id.value)

        if(len(result)==1):
            processors[result[0]].set_state(addr, "O")
        return len(result)

    def write_data(self, processors, addr, data):
        for proc in processors:
            if(proc.id.value != self.id.value):
                if(proc.read_cache(addr) is not None):
                    proc.write_cache(addr, data)
                else:
                    lines = proc.get_lines()
                    for line in lines:
                        if(line.tag is not None):
                            exclusive = True
                            for proc_2 in processors:
                                if(proc_2.id.value != proc.id.value):
                                    test_data = proc_2.read_cache(line.tag)
                                    if(test_data is not None):
                                        exclusive = False
                                        
                            if(exclusive):
                                proc.set_state(line.tag, "E")

    def inst_run(self, clk, bus, msg, data_found, processors):
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
                data = self.search_data(processors, inst_to_run.addr)
                if(data is not None):
                    data = data.data
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
            data = self.read_cache(inst_to_run.addr)
            print(f"CYCLE {start_clk}, PROC: {self.id.value}, WRITE", inst_to_run.addr, inst_to_run.data)
            while(clk.value-start_clk<=2):
                pass
            if(data is not None):
                self.write_cache(inst_to_run.addr, inst_to_run.data)
                self.write_data(processors, inst_to_run.addr, inst_to_run.data)
            else:
                data = self.search_data(processors, inst_to_run.addr)
                if(data is not None):
                    self.write_cache(inst_to_run.addr, inst_to_run.data)
                    self.set_state(inst_to_run.addr, "S")
                    self.write_data(processors, inst_to_run.addr, inst_to_run.data)
                else:
                    self.write_cache(inst_to_run.addr, inst_to_run.data) 
                    self.set_state(inst_to_run.addr, "E")
                    self.write_data(processors, inst_to_run.addr, inst_to_run.data)
            bus.write_mem(inst_to_run.addr, inst_to_run.data)
            self.inst.pop()
            bus.set_inst(None)
            bus.set_busy(False)
        elif(inst_type=="CALC"):
            print(f"CYCLE {clk.value}, PROC: {self.id.value}, CALC")
            self.inst.pop()

    def cpu_run(self, clk, bus, msg, kill, data_found, processors):
        clk_bef = 0 
        while(not kill.value):
            new_clk = clk.value
            if(clk_bef != new_clk):
                if(len(self.inst)==0):
                    self.new_inst()
                    #self.print_inst()
                else:
                    self.inst_run(clk, bus, msg, data_found, processors)

            clk_bef = new_clk
