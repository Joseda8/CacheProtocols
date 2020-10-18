import scipy.stats as ss
import numpy as np
import random

from time import time


def get_inst():
    rand_prob = 0.5
    rand_exp = 10

    X = ss.binom(rand_exp, rand_prob)
    #X = ss.poisson(rand_prob)
    #X = ss.hypergeom(30, rand_exp, 12)
    x = np.arange(3)

    prob_ins = []
    probs = X.pmf(x)
    for prob in probs:
        prob_ins.append(round(prob*100))

    inst = list(np.full(prob_ins[0], 0))+list(np.full(prob_ins[1], 1))+list(np.full(prob_ins[2], 2))
    random.shuffle(inst)

    return inst

start_time = time()
print(get_inst())
elapsed_time = time() - start_time
print(elapsed_time)
