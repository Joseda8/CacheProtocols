from processor import Processor
from bus import Bus
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
from queue import Queue 
from tkinter import *
from tkinter import font
from tkinter import messagebox

import util
import time
import threading
import multiprocessing
import sys


#Variables globales
clk = multiprocessing.Value('i') 
kill = multiprocessing.Value('i', False) 

#Funciones
def start_clk(clk, kill):
    while(not kill.value):
        #print("Writing", clk.value)
        clk.value += 1
        time.sleep(1.5)
    return

def reader(clk, bus, processors, kill):
    clk_bef = 0 
    while(not kill.value):
        new_clk = clk.value
        if(clk_bef != new_clk):
            tags["clk"].configure(text="CLK: "+str(new_clk))

            #Update bus
            bus_inst = bus.get_inst()
            if(bus_inst is not None):
                #print(f"BUS: PROC {bus_inst.proc_id} INST: {bus_inst.type}")
                tags["bus_inst"].configure(text=f"PROC: {bus_inst.proc_id}, {bus_inst}")

            #Update mem
            mem = bus.get_mem()
            i = 0
            for data in mem:
                tags[str(i)+"mem"].configure(text=hex(data))
                i += 1

            #Update processors
            for proc in processors:
                proc_inst = proc.get_inst_exe()
                if(proc_inst is not None):
                    #print(f"PROCESSOR {proc.id.value}, INST: {proc_inst.type}")
                    tags[str(proc.id.value)+"inst"].configure(text=proc_inst)
                lines = proc.get_lines()
                for line in lines:
                    #print(f"LINE {line.id}\nTAG: {line.tag}\nDATA: {line.data}\nSTATE: {line.state}")
                    tag = tags[line.name]
                    tag[0].configure(text=line.state)
                    tag[1].configure(text=line.tag)
                    tag[2].configure(text=line.data)

        clk_bef = new_clk
    return
                                        

def kill_threads():
    tags["100"][0].configure(text="E")
    tags["100"][1].configure(text="0000")
    tags["100"][2].configure(text="0xDDDDCCCC")
    tags["1inst"].configure(text="W 0000 0xCCCCDDDD")
    tags["6mem"].configure(text="0xCCCCDDDD")
    tags["bus_inst"].configure(text="PROC: 1, W 0000 0xABCG4632")

def exit():
    kill.value = True
    window.destroy()
    window.quit()
    util.sleep(2)
    sys.exit()

################################
########    MAIN    ############
################################

if __name__ == '__main__':


    window = Tk()
    window.title("Cache Protocols")

    tags = util.create_gui()

    exit_btn = Button(window, text="Exit", command= exit, background='white', fg='blue')
    exit_btn.place(x=1150, y=560)

    #Instancias de los componentes
    BaseManager.register('Bus', Bus)
    bus_manager = BaseManager()
    bus_manager.start()
    bus = bus_manager.Bus()

    msg = Queue() 

    #processors = [Processor(1), Processor(2), Processor(3), Processor(4)]
    processors = [Processor(1), Processor(2)]

    threads = [threading.Thread(target=start_clk, args=(clk, kill)), threading.Thread(target=reader, args=(clk, bus, processors, kill))]
    #threads = [threading.Thread(target=start_clk, args=(clk, kill))]

    for proc in processors:
        threads.append(threading.Thread(target=proc.cpu_run, args=(clk, bus, msg, kill)))
        threads.append(threading.Thread(target=proc.snoopy, args=(clk, bus, msg, processors, kill)))

    [t.start() for t in threads]
    #threads.append(msg)
    #[t.join() for t in threads]
    
    window.mainloop()

