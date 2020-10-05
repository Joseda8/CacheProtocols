import processor
import memory
import time
import threading
import multiprocessing 

#Variables globales
clk = multiprocessing.Value('i') 

#Funciones
def start_clk(clk):
    while(True):
        print("Writing")
        clk.value += 1
        time.sleep(1.5)

def read_clk(clk):
    while(True):
        print("Read: ", clk.value)
        time.sleep(1.5)



################################
########    MAIN    ############
################################

#Instancias de los componentes
memory = memory.Memory()
processor_1 = processor.Processor(1)
processor_2 = processor.Processor(2)
processor_3 = processor.Processor(3)
processor_4 = processor.Processor(4)

x = processor_1.get_data(8)
print(x)

threads = [threading.Thread(target=start_clk, args=(clk,)), threading.Thread(target=read_clk, args=(clk,))]
[t.start() for t in threads]
[t.join() for t in threads]