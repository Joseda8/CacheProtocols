import scipy.stats as ss
import numpy as np
import random

rand_num = random.random()

X = ss.binom(3, rand_num)
x = np.arange(3)

prob_ins = []
probs = X.pmf(x)
for prob in probs:
    prob_ins.append(round(prob*100))

inst = list(np.full(prob_ins[0], 0))+list(np.full(prob_ins[1], 1))+list(np.full(prob_ins[2], 2))
random.shuffle(inst)
rand_ins = random.randint(0, len(inst)-1)

print(inst)
print(rand_ins)
print(inst[rand_ins])
