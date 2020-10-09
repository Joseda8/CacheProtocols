import scipy.stats as ss
import numpy as np
import random
import time
from queue import Queue 


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