from processor import Processor
from bus import Bus
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from ctypes import c_char_p

import instruction
import util
import time
import threading
import multiprocessing
import sys


#Variables globales
clk = multiprocessing.Value('i') 
kill = multiprocessing.Value('i', False) 
pause = multiprocessing.Value('i', True)
mode = None
steps = None
time_to_sleep = 2.5

data_found = multiprocessing.Value('i', False)

#Funciones
def start_clk(clk, kill):
    global mode
    while(not kill.value):
        if(mode=="Ciclos"):
            i = 1
            while(not pause.value):
                if(i>=steps):
                    pause_btn.configure(text="Play")
                    pause.value = True
                i += 1
                clk.value += 1
                time.sleep(time_to_sleep)
        elif(mode=="Siguiente"):
            clk.value += 1
            time.sleep(time_to_sleep)
            pause_btn.configure(text="Play")
            pause.value = True
            mode = None
        elif(mode=="Continua"):
            while(not pause.value):
                clk.value += 1
                time.sleep(time_to_sleep)
    return

def pause_clk():
    if(pause.value):
        global mode
        global steps
        mode = mode_option["values"][mode_option.current()]
        steps = int(steps_option["values"][steps_option.current()])
        pause_btn.configure(text="Pause")
    else:
        pause_btn.configure(text="Play") 
    pause.value = not pause.value   

def reader(clk, bus, processors, kill):
    while(not kill.value):
        tags["clk"].configure(text="CLK: "+str(clk.value))

        #Update bus
        bus_inst = bus.get_inst()
        if(bus_inst is not None):
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
                tags[str(proc.id.value)+"inst"].configure(text=proc_inst)
            lines = proc.get_lines()
            for line in lines:
                tag = tags[line.name]
                tag[0].configure(text=line.state)
                if(line.tag is not None):
                    tag[1].configure(text=bin(line.tag)[2:])
                tag[2].configure(text=hex(line.data))
    return


def set_instructions():
    line = open("instruction.txt", "r").readline()
    proc = int(line[0])
    inst_type = line[1]
    addr = int(line[2:4])
    data = int(line[4:6])

    info = None

    if(inst_type=="R"):
        inst_type = "READ"
        info = [addr]
    elif(inst_type=="W"):
        inst_type="WRITE"
        info = [addr, data]
    else:
        inst_type="CALC"

    processors[proc-1].add_inst(instruction.Instruction(proc, inst_type, info))

def exit():
    kill.value = True
    """
    window.destroy()
    window.quit()
    sys.exit()
    """
    
################################
########    MAIN    ############
################################

if __name__ == '__main__':


    window = Tk()
    window.title("Cache Protocols")

    tags = util.create_gui()

    mode_option = ttk.Combobox(width=15)
    mode_option.place(x=150, y=560)
    mode_option["values"] = ["Ciclos", "Siguiente", "Continua"]

    steps_option = ttk.Combobox(width=2)
    steps_option.place(x=260, y=560)
    steps_option["values"] = [1, 2, 3, 4, 5]

    pause_btn = Button(window, text="Start", command= pause_clk, background='white', fg='blue')
    pause_btn.place(x=320, y=560)

    add_btn = Button(window, text="Add Instruction", command= set_instructions, background='white', fg='blue')
    add_btn.place(x=380, y=560)

    exit_btn = Button(window, text="Exit", command= exit, background='white', fg='blue')
    exit_btn.place(x=1100, y=560)

    #Instancias de los componentes
    BaseManager.register('Bus', Bus)
    bus_manager = BaseManager()
    bus_manager.start()
    bus = bus_manager.Bus()

    processors = [Processor(1), Processor(2), Processor(3), Processor(4)]
    #processors = [Processor(1), Processor(2)]

    threads = [threading.Thread(target=start_clk, args=(clk, kill)), threading.Thread(target=reader, args=(clk, bus, processors, kill))]

    for proc in processors:
        threads.append(threading.Thread(target=proc.cpu_run, args=(clk, bus, kill, processors)))
    
    [t.start() for t in threads]
    
    window.mainloop()

