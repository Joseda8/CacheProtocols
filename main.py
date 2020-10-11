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
        time.sleep(1.5)


def reader(clk, bus, processors):
    clk_bef = 0 
    while(True):
        new_clk = clk.value
        if(clk_bef != new_clk):
            bus_inst = bus.get_inst()
            if(bus_inst is not None):
                print(f"BUS: PROC {bus_inst.proc_id} INST: {bus_inst.type}")
            for proc in processors:
                proc_inst = proc.get_inst_exe()
                if(proc_inst is not None):
                    print(f"PROCESSOR {proc.id.value}, INST: {proc_inst.type}")
                lines = proc.get_lines()
                for line in lines:
                    print(f"LINE {line.id}\nTAG: {line.tag}\nDATA: {line.data}\nSTATE: {line.state}")

        clk_bef = new_clk
                                        

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

    #processors = [Processor(1), Processor(2), Processor(3), Processor(4)]
    #processors = [Processor(1)]
    processors = [Processor(1), Processor(2)]

    #threads = [threading.Thread(target=start_clk, args=(clk,)), threading.Thread(target=check_bus, args=(processors, msg, check_flag))]
    threads = [threading.Thread(target=start_clk, args=(clk,)), threading.Thread(target=reader, args=(clk, bus, processors))]

    for proc in processors:
        threads.append(threading.Thread(target=proc.cpu_run, args=(clk, bus, msg)))
        threads.append(threading.Thread(target=proc.snoopy, args=(clk, bus, msg)))

    [t.start() for t in threads]
    #threads.append(msg)
    #[t.join() for t in threads]
    



