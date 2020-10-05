from PIL import Image
from PIL import ImageFilter
from time import time
import numpy as np
import threading
import sys


def sharp(img_list):
    global times
    start_time = time()
    for img in img_list:
        img.img.filter(ImageFilter.SHARPEN)
    elapsed_time = time() - start_time
    times.append(elapsed_time)

def check_threads(threads):
    for t in threads:
        if(t.isAlive()):
            check_threads(threads)
        else:
            threads.remove(t)

class myImage:
    def __init__(self, filename):
        img_aux = Image.open(filename)
        pixels_list = np.asarray(img_aux)
        img_aux.close()
        self.img = Image.fromarray(pixels_list)
        self.name = filename

sys.setrecursionlimit(20000)
image_list = []
objects = 400
threads_num = 10
objects_threads = int(objects/threads_num)
times = []

i = 0
while i<=objects:
    image_list.append(myImage("lucario.jpg"))
    i+=1
    
threads = []
i = 0
while i<threads_num:
    t = threading.Thread(target=sharp,
                         args=(image_list[i*objects_threads:(i+1)*objects_threads-1],))
    threads.append(t)
    i+=1

[t.start() for t in threads]
[t.join() for t in threads]

total_time = 0
for time in times:
    total_time += time
print("Tiempo transcurrido: %0.10f seconds." % total_time)
