from processor import Processor
from bus import Bus
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
from queue import Queue 

import time
import threading
import multiprocessing
import sys


#Variables globales
clk = multiprocessing.Value('i') 

#Funciones
def start_clk(clk):
    while(True):
        #print("Writing", clk.value)
        clk.value += 1
        time.sleep(0.5)

def read_clk(clk):
    while(True):
        print("Read: ", clk.value)
        time.sleep(1.5)

def read_test(proc):
    while(True):
        print(proc.inst)
        time.sleep(1.0)



################################
########    MAIN    ############
################################

if __name__ == '__main__':

    #Instancias de los componentes
    BaseManager.register('Bus', Bus)
    manager = BaseManager()
    manager.start()
    bus = manager.Bus()

    msg = Queue() 

    #processors = [Processor(1), Processor(2), Processor(3), Processor(4)]
    #processors = [Processor(1)]
    processors = [Processor(1), Processor(2)]

    threads = [threading.Thread(target=start_clk, args=(clk,))]

    for proc in processors:
        threads.append(threading.Thread(target=proc.cpu_run, args=(clk, bus, msg)))
        threads.append(threading.Thread(target=proc.snoopy, args=(clk, bus, msg)))

    [t.start() for t in threads]
    threads.append(msg)
    [t.join() for t in threads]
