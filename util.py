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
    tags = {}
    
    Helvfont = font.Font(family="Helvetica", size=12, weight="bold")
    Helvfont_inst = font.Font(family="Helvetica", size=10, weight="bold")
    canvas = Canvas(width=1200, height=600, bg='lightgray')
    canvas.pack()

    #CACHE 1
    canvas.create_rectangle(25, 25, 300, 255, fill="lightblue", outline="blue")

    canvas.create_rectangle(40, 40, 285, 80, fill="white", outline="black") #DATA
    canvas.create_rectangle(40, 40, 85, 80, fill="white", outline="black") #STATE
    canvas.create_rectangle(85, 40, 160, 80, fill="white", outline="black") #TAG
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=62.5, y=60, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=122.5, y=60, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=222.5, y=60, anchor='center')
    tags["100"] = (state, tag, data)

    canvas.create_rectangle(40, 80, 285, 120, fill="white", outline="black")
    canvas.create_rectangle(40, 80, 85, 120, fill="white", outline="black")
    canvas.create_rectangle(85, 80, 160, 120, fill="white", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=62.5, y=100, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=122.5, y=100, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=222.5, y=100, anchor='center')
    tags["101"] = (state, tag, data)

    canvas.create_rectangle(40, 120, 285, 160, fill="gray90", outline="black")
    canvas.create_rectangle(40, 120, 85, 160, fill="gray90", outline="black")
    canvas.create_rectangle(85, 120, 160, 160, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=62.5, y=140, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=122.5, y=140, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=222.5, y=140, anchor='center')
    tags["110"] = (state, tag, data)

    canvas.create_rectangle(40, 160, 285, 200, fill="gray90", outline="black")
    canvas.create_rectangle(40, 160, 85, 200, fill="gray90", outline="black")
    canvas.create_rectangle(85, 160, 160, 200, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=62.5, y=180, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=122.5, y=180, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=222.5, y=180, anchor='center')
    tags["111"] = (state, tag, data)

    canvas.create_rectangle(40, 200, 285, 240, fill="lightyellow", outline="black") 
    canvas.create_rectangle(40, 200, 85, 240, fill="lightyellow", outline="black")
    Label(canvas, text="1", font=Helvfont, fg='black', background='lightyellow').place(x=62, y=220, anchor='center')
    inst = Label(canvas, text="", font=Helvfont_inst, fg='black', background='lightyellow')
    inst.place(x=185, y=220, anchor='center')
    tags["1inst"] = inst


    #CACHE 2
    canvas.create_rectangle(25, 275, 300, 505, fill="lightblue", outline="blue")

    canvas.create_rectangle(40, 290, 285, 330, fill="white", outline="black") #DATA
    canvas.create_rectangle(40, 290, 85, 330, fill="white", outline="black") #STATE
    canvas.create_rectangle(85, 290, 160, 330, fill="white", outline="black") #TAG
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=62.5, y=310, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=122.5, y=310, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=222.5, y=310, anchor='center')
    tags["200"] = (state, tag, data)

    canvas.create_rectangle(40, 330, 285, 370, fill="white", outline="black")
    canvas.create_rectangle(40, 330, 85, 370, fill="white", outline="black")
    canvas.create_rectangle(85, 330, 160, 370, fill="white", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=62.5, y=350, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=122.5, y=350, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=222.5, y=350, anchor='center')
    tags["201"] = (state, tag, data)

    canvas.create_rectangle(40, 370, 285, 410, fill="gray90", outline="black")
    canvas.create_rectangle(40, 370, 85, 410, fill="gray90", outline="black")
    canvas.create_rectangle(85, 370, 160, 410, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=62.5, y=390, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=122.5, y=390, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=222.5, y=390, anchor='center')
    tags["210"] = (state, tag, data)

    canvas.create_rectangle(40, 410, 285, 450, fill="gray90", outline="black")
    canvas.create_rectangle(40, 410, 85, 450, fill="gray90", outline="black")
    canvas.create_rectangle(85, 410, 160, 450, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=62.5, y=430, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=122.5, y=430, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=222.5, y=430, anchor='center')
    tags["211"] = (state, tag, data)

    canvas.create_rectangle(40, 450, 285, 490, fill="lightyellow", outline="black")
    canvas.create_rectangle(40, 450, 85, 490, fill="lightyellow", outline="black")
    Label(canvas, text="2", font=Helvfont, fg='black', background='lightyellow').place(x=62, y=470, anchor='center')
    inst = Label(canvas, text="", font=Helvfont_inst, fg='black', background='lightyellow')
    inst.place(x=185, y=470, anchor='center')
    tags["2inst"] = inst

    #CACHE 3
    canvas.create_rectangle(325, 25, 600, 255, fill="lightblue", outline="blue")

    canvas.create_rectangle(340, 40, 585, 80, fill="white", outline="black") #DATA
    canvas.create_rectangle(340, 40, 385, 80, fill="white", outline="black") #STATE
    canvas.create_rectangle(385, 40, 460, 80, fill="white", outline="black") #TAG
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=362.5, y=60, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=422.5, y=60, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=522.5, y=60, anchor='center')
    tags["300"] = (state, tag, data)

    canvas.create_rectangle(340, 80, 585, 120, fill="white", outline="black")
    canvas.create_rectangle(340, 80, 385, 120, fill="white", outline="black")
    canvas.create_rectangle(385, 80, 460, 120, fill="white", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=362.5, y=100, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=422.5, y=100, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=522.5, y=100, anchor='center')
    tags["301"] = (state, tag, data)

    canvas.create_rectangle(340, 120, 585, 160, fill="gray90", outline="black")
    canvas.create_rectangle(340, 120, 385, 160, fill="gray90", outline="black")
    canvas.create_rectangle(385, 120, 460, 160, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=362.5, y=140, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=422.5, y=140, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=522.5, y=140, anchor='center')
    tags["310"] = (state, tag, data)

    canvas.create_rectangle(340, 160, 585, 200, fill="gray90", outline="black")
    canvas.create_rectangle(340, 160, 385, 200, fill="gray90", outline="black")
    canvas.create_rectangle(385, 160, 460, 200, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=362.5, y=180, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=422.5, y=180, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=522.5, y=180, anchor='center')
    tags["311"] = (state, tag, data)

    canvas.create_rectangle(340, 200, 585, 240, fill="lightyellow", outline="black")
    canvas.create_rectangle(340, 200, 385, 240, fill="lightyellow", outline="black")
    Label(canvas, text="3", font=Helvfont, fg='black', background='lightyellow').place(x=362, y=220, anchor='center')
    inst = Label(canvas, text="", font=Helvfont_inst, fg='black', background='lightyellow')
    inst.place(x=485, y=220, anchor='center')
    tags["3inst"] = inst

    #CACHE 4
    canvas.create_rectangle(325, 275, 600, 505, fill="lightblue", outline="blue")

    canvas.create_rectangle(340, 290, 585, 330, fill="white", outline="black") #DATA
    canvas.create_rectangle(340, 290, 385, 330, fill="white", outline="black") #STATE
    canvas.create_rectangle(385, 290, 460, 330, fill="white", outline="black") #TAG
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=362.5, y=310, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=422.5, y=310, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=522.5, y=310, anchor='center')
    tags["400"] = (state, tag, data)

    canvas.create_rectangle(340, 330, 585, 370, fill="white", outline="black")
    canvas.create_rectangle(340, 330, 385, 370, fill="white", outline="black")
    canvas.create_rectangle(385, 330, 460, 370, fill="white", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    state.place(x=362.5, y=350, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    tag.place(x=422.5, y=350, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=522.5, y=350, anchor='center')
    tags["401"] = (state, tag, data)

    canvas.create_rectangle(340, 370, 585, 410, fill="gray90", outline="black")
    canvas.create_rectangle(340, 370, 385, 410, fill="gray90", outline="black")
    canvas.create_rectangle(385, 370, 460, 410, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=362.5, y=390, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=422.5, y=390, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=522.5, y=390, anchor='center')
    tags["410"] = (state, tag, data)

    canvas.create_rectangle(340, 410, 585, 450, fill="gray90", outline="black")
    canvas.create_rectangle(340, 410, 385, 450, fill="gray90", outline="black")
    canvas.create_rectangle(385, 410, 460, 450, fill="gray90", outline="black")
    state = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    state.place(x=362.5, y=430, anchor='center')
    tag = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    tag.place(x=422.5, y=430, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=522.5, y=430, anchor='center')
    tags["410"] = (state, tag, data)

    canvas.create_rectangle(340, 450, 585, 490, fill="lightyellow", outline="black")
    canvas.create_rectangle(340, 450, 385, 490, fill="lightyellow", outline="black")
    Label(canvas, text="4", font=Helvfont, fg='black', background='lightyellow').place(x=362, y=470, anchor='center')
    inst = Label(canvas, text="", font=Helvfont_inst, fg='black', background='lightyellow')
    inst.place(x=485, y=470, anchor='center')
    tags["4inst"] = inst


    #MEMORY
    canvas.create_rectangle(650, 25, 1175, 410, fill="lightpink", outline="red")

    canvas.create_rectangle(665, 40, 912.5, 80, fill="white", outline="black") #DATA
    canvas.create_rectangle(665, 40, 740, 80, fill="white", outline="black") #TAG
    canvas.create_rectangle(912.5, 40, 1160, 80, fill="gray90", outline="black") #DATA
    canvas.create_rectangle(912.5, 40, 987.5, 80, fill="gray90", outline="black") #TAG
    Label(canvas, text="0000", font=Helvfont, fg='black', background='white').place(x=702.5, y=60, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=60, anchor='center')
    tags["0mem"] = data
    Label(canvas, text="0001", font=Helvfont, fg='black', background='gray90').place(x=950, y=60, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=60, anchor='center')
    tags["1mem"] = data

    canvas.create_rectangle(665, 80, 912.5, 120, fill="white", outline="black")
    canvas.create_rectangle(665, 80, 740, 120, fill="white", outline="black")
    canvas.create_rectangle(912.5, 80, 1160, 120, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 80, 987.5, 120, fill="gray90", outline="black")
    Label(canvas, text="0010", font=Helvfont, fg='black', background='white').place(x=702.5, y=100, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=100, anchor='center')
    tags["2mem"] = data
    Label(canvas, text="0011", font=Helvfont, fg='black', background='gray90').place(x=950, y=100, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=100, anchor='center')
    tags["3mem"] = data

    canvas.create_rectangle(665, 120, 912.5, 160, fill="white", outline="black")
    canvas.create_rectangle(665, 120, 740, 160, fill="white", outline="black")
    canvas.create_rectangle(912.5, 120, 1160, 160, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 120, 987.5, 160, fill="gray90", outline="black")
    Label(canvas, text="0100", font=Helvfont, fg='black', background='white').place(x=702.5, y=140, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=140, anchor='center')
    tags["4mem"] = data
    Label(canvas, text="0101", font=Helvfont, fg='black', background='gray90').place(x=950, y=140, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=140, anchor='center')
    tags["5mem"] = data

    canvas.create_rectangle(665, 160, 912.5, 200, fill="white", outline="black")
    canvas.create_rectangle(665, 160, 740, 200, fill="white", outline="black")
    canvas.create_rectangle(912.5, 160, 1160, 200, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 160, 987.5, 200, fill="gray90", outline="black")
    Label(canvas, text="0110", font=Helvfont, fg='black', background='white').place(x=702.5, y=180, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=180, anchor='center')
    tags["6mem"] = data
    Label(canvas, text="0111", font=Helvfont, fg='black', background='gray90').place(x=950, y=180, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=180, anchor='center')
    tags["7mem"] = data

    canvas.create_rectangle(665, 200, 912.5, 240, fill="white", outline="black")
    canvas.create_rectangle(665, 200, 740, 240, fill="white", outline="black")
    canvas.create_rectangle(912.5, 200, 1160, 240, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 200, 987.5, 240, fill="gray90", outline="black")
    Label(canvas, text="1000", font=Helvfont, fg='black', background='white').place(x=702.5, y=220, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=220, anchor='center')
    tags["8mem"] = data
    Label(canvas, text="1001", font=Helvfont, fg='black', background='gray90').place(x=950, y=220, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=220, anchor='center')
    tags["9mem"] = data

    canvas.create_rectangle(665, 240, 912.5, 280, fill="white", outline="black")
    canvas.create_rectangle(665, 240, 740, 280, fill="white", outline="black")
    canvas.create_rectangle(912.5, 240, 1160, 280, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 240, 987.5, 280, fill="gray90", outline="black")
    Label(canvas, text="1010", font=Helvfont, fg='black', background='white').place(x=702.5, y=260, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=260, anchor='center')
    tags["10mem"] = data
    Label(canvas, text="1011", font=Helvfont, fg='black', background='gray90').place(x=950, y=260, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=260, anchor='center')
    tags["11mem"] = data

    canvas.create_rectangle(665, 280, 912.5, 320, fill="white", outline="black")
    canvas.create_rectangle(665, 280, 740, 320, fill="white", outline="black")
    canvas.create_rectangle(912.5, 280, 1160, 320, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 280, 987.5, 320, fill="gray90", outline="black")
    Label(canvas, text="1100", font=Helvfont, fg='black', background='white').place(x=702.5, y=300, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=300, anchor='center')
    tags["12mem"] = data
    Label(canvas, text="1101", font=Helvfont, fg='black', background='gray90').place(x=950, y=300, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=300, anchor='center')
    tags["13mem"] = data

    canvas.create_rectangle(665, 320, 912.5, 360, fill="white", outline="black")
    canvas.create_rectangle(665, 320, 740, 360, fill="white", outline="black")
    canvas.create_rectangle(912.5, 320, 1160, 360, fill="gray90", outline="black")
    canvas.create_rectangle(912.5, 320, 987.5, 360, fill="gray90", outline="black")
    Label(canvas, text="1110", font=Helvfont, fg='black', background='white').place(x=702.5, y=340, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='white')
    data.place(x=826.25, y=340, anchor='center')
    tags["14mem"] = data
    Label(canvas, text="1111", font=Helvfont, fg='black', background='gray90').place(x=950, y=340, anchor='center')
    data = Label(canvas, text="", font=Helvfont, fg='black', background='gray90')
    data.place(x=1073.75, y=340, anchor='center')
    tags["15mem"] = data

    Label(canvas, text="Memory", font=Helvfont, fg='black', background='lightpink').place(x=697.5, y=385, anchor='center')

    #BUS
    canvas.create_rectangle(650, 425, 1175, 505, fill="lightgreen", outline="green")
    Label(canvas, text="Bus", font=Helvfont, fg='black', background='lightgreen').place(x=697.5, y=480, anchor='center')
    inst = Label(canvas, text="", font=Helvfont, fg='black', background='lightgreen')
    inst.place(x=912.5, y=465, anchor='center')
    tags["bus_inst"] = inst

    #CLK
    data = Label(canvas, text="CLK: 0", font=Helvfont, fg='black', background='lightgray')
    data.place(x=50, y=575, anchor='center')
    tags["clk"] = data

    return tags