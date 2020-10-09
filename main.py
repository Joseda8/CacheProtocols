from processor import Processor
from bus import Bus
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
from queue import Queue 

import util
import time
import threading
import multiprocessing
import sys


#Variables globales
clk = multiprocessing.Value('i') 
check_flag = multiprocessing.Value('i') 

#Funciones
def start_clk(clk):
    while(True):
        #print("Writing", clk.value)
        clk.value += 1
        time.sleep(2)


def check_bus(processors, msg, check_flag):
    while(True):
        new_msg = util.get_msg(msg)
        inst = new_msg["req"]
        if(inst.type=="WRITE" and check_flag.value):
            addr = inst.addr
            proc_id = inst.proc_id
            for proc in processors:
                state = None
                if(proc.id != proc_id):
                    lines = proc.get_lines()
                    for line in lines:
                        if(line.tag is not None):
                            state = True
                            for proc_aux in processors:
                                if(proc.id != proc_aux.id):
                                    if(proc_aux.read_cache(line.tag) is not None):
                                        state = False
                if(state):
                    proc.set_state(addr, "E")
            util.clear_msg(msg)
            check_flag.value = False

                                        

################################
########    MAIN    ############
################################

if __name__ == '__main__':

    #Instancias de los componentes
    BaseManager.register('Bus', Bus)
    bus_manager = BaseManager()
    bus_manager.start()
    bus = bus_manager.Bus()

    msg = Queue() 

    processors = [Processor(1), Processor(2), Processor(3), Processor(4)]
    #processors = [Processor(1)]
    #processors = [Processor(1), Processor(2)]

    #threads = [threading.Thread(target=start_clk, args=(clk,)), threading.Thread(target=check_bus, args=(processors, msg, check_flag))]
    threads = [threading.Thread(target=start_clk, args=(clk,))]

    for proc in processors:
        threads.append(threading.Thread(target=proc.cpu_run, args=(clk, bus, msg)))
        threads.append(threading.Thread(target=proc.snoopy, args=(clk, bus, msg)))

    [t.start() for t in threads]
    threads.append(msg)
    [t.join() for t in threads]


