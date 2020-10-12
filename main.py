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
    return
                                        

def kill_threads():
    tags[0].configure(text="FUMADOS")

def exit():
    kill.value = True
    window.destroy()
    window.quit()
    sys.exit()

################################
########    MAIN    ############
################################

if __name__ == '__main__':


    window = Tk()
    window.title("Cache Protocols")

    util.create_gui()

    exit_btn = Button(window, text="Exit", command= exit, background='white', fg='blue')
    exit_btn.place(x=1100, y=500)

    btn = Button(window, text="Aceptar", command= kill_threads, background='white', fg='blue')
    btn.place(x=275, y=185)

    Helvfont = font.Font(family="Helvetica", size=12, weight="bold")
    lbl = Label(window, text="HOLANGAS", font=Helvfont, fg='blue', background='white')
    lbl.place(x=700, y=380, anchor='center')

    tags = [lbl]
    
    """
    greeting = Label(window,
            text="¡Hola! \n Bienvenido al mundo Pokémon. \n Mi nombre es Samuel Oak, pero todos me conocen como el Profesor Oak. \n\n Basta de hablar sobre mí, cuéntame algo sobre tí. \n ¿Cómo te llamas?",
            font=Helvfont, fg='blue', background='white')

    greeting.place(x=20, y=20)
    """

    #Instancias de los componentes
    BaseManager.register('Bus', Bus)
    bus_manager = BaseManager()
    bus_manager.start()
    bus = bus_manager.Bus()

    msg = Queue() 

    #processors = [Processor(1), Processor(2), Processor(3), Processor(4)]
    processors = [Processor(1), Processor(2)]

    #threads = [threading.Thread(target=start_clk, args=(clk,)), threading.Thread(target=reader, args=(clk, bus, processors, kill))]
    threads = [threading.Thread(target=start_clk, args=(clk, kill))]

    for proc in processors:
        threads.append(threading.Thread(target=proc.cpu_run, args=(clk, bus, msg, kill)))
        threads.append(threading.Thread(target=proc.snoopy, args=(clk, bus, msg, processors, kill)))

    [t.start() for t in threads]
    #threads.append(msg)
    #[t.join() for t in threads]
    
    window.mainloop()

