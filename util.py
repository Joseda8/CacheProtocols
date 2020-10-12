import scipy.stats as ss
import numpy as np
import random
import time
from queue import Queue 
from tkinter import *
from tkinter import font
from tkinter import messagebox

def get_inst():
    rand_prob = random.random()
    rand_exp = random.randint(1, 10)

    X = ss.binom(rand_exp, rand_prob)
    #X = ss.poisson(rand_prob)
    x = np.arange(3)

    prob_ins = []
    probs = X.pmf(x)
    for prob in probs:
        prob_ins.append(round(prob*100))

    inst = list(np.full(prob_ins[0], 0))+list(np.full(prob_ins[1], 1))+list(np.full(prob_ins[2], 2))
    random.shuffle(inst)

    return inst
    
def get_randint(lowest, highest):
    return random.randint(lowest, highest)

def sleep(seconds):
    time.sleep(seconds)


def clear_msg(msg):
    while(not msg.empty()):
        msg.get()
        msg.task_done()

def insert_msg(msg, req, ans, status):
    clear_msg(msg)
    msg.put({"req": req, "ans": ans, "status": status})

def get_msg(msg):
    new_msg = msg.get()
    msg.task_done()
    insert_msg(msg, new_msg["req"], new_msg["ans"], new_msg["status"])
    return new_msg

def create_gui():
    canvas = Canvas(width=1200, height=600, bg='lightgray')
    canvas.pack()

    #CACHE 1
    canvas.create_rectangle(25, 25, 300, 255, fill="lightblue", outline="blue")

    canvas.create_rectangle(40, 40, 285, 80, fill="white", outline="black")
    canvas.create_rectangle(40, 40, 85, 80, fill="white", outline="black")
    canvas.create_rectangle(85, 40, 160, 80, fill="white", outline="black")

    canvas.create_rectangle(40, 80, 285, 120, fill="white", outline="black")
    canvas.create_rectangle(40, 80, 85, 120, fill="white", outline="black")
    canvas.create_rectangle(85, 80, 160, 120, fill="white", outline="black")

    canvas.create_rectangle(40, 120, 285, 160, fill="gray90", outline="black")
    canvas.create_rectangle(40, 120, 85, 160, fill="gray90", outline="black")
    canvas.create_rectangle(85, 120, 160, 160, fill="gray90", outline="black")

    canvas.create_rectangle(40, 160, 285, 200, fill="gray90", outline="black")
    canvas.create_rectangle(40, 160, 85, 200, fill="gray90", outline="black")
    canvas.create_rectangle(85, 160, 160, 200, fill="gray90", outline="black")

    canvas.create_rectangle(40, 200, 285, 240, fill="lightyellow", outline="black")

    #CACHE 2
    canvas.create_rectangle(25, 275, 300, 505, fill="lightblue", outline="blue")

    canvas.create_rectangle(40, 290, 285, 330, fill="white", outline="black")
    canvas.create_rectangle(40, 290, 85, 330, fill="white", outline="black")
    canvas.create_rectangle(85, 290, 160, 330, fill="white", outline="black")

    canvas.create_rectangle(40, 330, 285, 370, fill="white", outline="black")
    canvas.create_rectangle(40, 330, 85, 370, fill="white", outline="black")
    canvas.create_rectangle(85, 330, 160, 370, fill="white", outline="black")

    canvas.create_rectangle(40, 370, 285, 410, fill="gray90", outline="black")
    canvas.create_rectangle(40, 370, 85, 410, fill="gray90", outline="black")
    canvas.create_rectangle(85, 370, 160, 410, fill="gray90", outline="black")

    canvas.create_rectangle(40, 410, 285, 450, fill="gray90", outline="black")
    canvas.create_rectangle(40, 410, 85, 450, fill="gray90", outline="black")
    canvas.create_rectangle(85, 410, 160, 450, fill="gray90", outline="black")

    canvas.create_rectangle(40, 450, 285, 490, fill="lightyellow", outline="black")

    #CACHE 3
    canvas.create_rectangle(325, 25, 600, 255, fill="lightblue", outline="blue")

    canvas.create_rectangle(340, 40, 585, 80, fill="white", outline="black")
    canvas.create_rectangle(340, 40, 385, 80, fill="white", outline="black")
    canvas.create_rectangle(385, 40, 460, 80, fill="white", outline="black")

    canvas.create_rectangle(340, 80, 585, 120, fill="white", outline="black")
    canvas.create_rectangle(340, 80, 385, 120, fill="white", outline="black")
    canvas.create_rectangle(385, 80, 460, 120, fill="white", outline="black")

    canvas.create_rectangle(340, 120, 585, 160, fill="gray90", outline="black")
    canvas.create_rectangle(340, 120, 385, 160, fill="gray90", outline="black")
    canvas.create_rectangle(385, 120, 460, 160, fill="gray90", outline="black")

    canvas.create_rectangle(340, 160, 585, 200, fill="gray90", outline="black")
    canvas.create_rectangle(340, 160, 385, 200, fill="gray90", outline="black")
    canvas.create_rectangle(385, 160, 460, 200, fill="gray90", outline="black")

    canvas.create_rectangle(340, 200, 585, 240, fill="lightyellow", outline="black")

    #CACHE 4
    canvas.create_rectangle(325, 275, 600, 505, fill="lightblue", outline="blue")

    canvas.create_rectangle(340, 290, 585, 330, fill="white", outline="black")
    canvas.create_rectangle(340, 290, 385, 330, fill="white", outline="black")
    canvas.create_rectangle(385, 290, 460, 330, fill="white", outline="black")

    canvas.create_rectangle(340, 330, 585, 370, fill="white", outline="black")
    canvas.create_rectangle(340, 330, 385, 370, fill="white", outline="black")
    canvas.create_rectangle(385, 330, 460, 370, fill="white", outline="black")

    canvas.create_rectangle(340, 370, 585, 410, fill="gray90", outline="black")
    canvas.create_rectangle(340, 370, 385, 410, fill="gray90", outline="black")
    canvas.create_rectangle(385, 370, 460, 410, fill="gray90", outline="black")

    canvas.create_rectangle(340, 410, 585, 450, fill="gray90", outline="black")
    canvas.create_rectangle(340, 410, 385, 450, fill="gray90", outline="black")
    canvas.create_rectangle(385, 410, 460, 450, fill="gray90", outline="black")

    canvas.create_rectangle(340, 450, 585, 490, fill="lightyellow", outline="black")


    #MEMORY AND BUS
    canvas.create_rectangle(650, 25, 1175, 410, fill="lightpink", outline="red")
    canvas.create_rectangle(650, 425, 1175, 505, fill="lightgreen", outline="green")