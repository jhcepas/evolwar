import numpy as np
import subprocess
from collections import namedtuple
from random import randint, random, choice
from copy import deepcopy
from collections import defaultdict, Counter

from redcode import parse, OPCODES, MODIFIERS, MODES, Instruction


def duplicate(instructions, dup_size, dup_dist):
    start = randint(0, len(instructions))
    end = randint(start+1, start+dup_size+1)
    insert_point = randint(start+1, start+dup_dist)
    instructions[insert_point:insert_point] = instructions[start:end]

def delete(instructions, loss_size):
    start = randint(0, len(instructions))
    end = randint(start+1, start+loss_size+1)
    instructions[start:end] = []
    
def evolve(warrior):
    mutator = np.zeros(8)
    #mutator = [0.0005, 0.001, 0.001, 0.01, 0.01, 0.001, 0.001, 0.001]
    instructions = warrior.instructions

    mutator[randint(0, 3)] = 1.0
    
    mutated = False
    
    # Duplications
    prob_duplication = mutator[0]
    dup_size_values = range(1, 10)
    dup_distance_values = range(1, 10)
    if random() < prob_duplication:
        mutated = True
        dup_size = choice(dup_size_values)
        dup_dist = choice(dup_distance_values)        
        duplicate(instructions, dup_size, dup_dist)

    # Deletions
    prob_deletion = mutator[1]
    del_size = range(1, 2)    
    if random() < prob_deletion:
        mutated = True
        loss_size = choice(dup_size_values)
        loss_dist = choice(dup_distance_values)        
        delete(instructions, loss_size)

    # Point mutations
    position_values = {
        0: OPCODES,
        1: MODIFIERS,
        2: MODES,
        3: range(-10, 10),
        4: MODES,
        5: range(-10, 10),
    }

    if len(instructions):
        inst_index = randint(0, len(instructions)-1)
        prob_mutation = mutator[2:8]
        inst = list(instructions[inst_index])
        for i, mut_rate in enumerate(prob_mutation):
            if random() < mut_rate:
                mutated = True
                values = position_values[i]
                inst[i] = choice(values)
        instructions[inst_index] = Instruction(*inst)

    return mutated

def pmars(w1, w2, rounds):
    with open('/tmp/w1', 'w') as W1:
        with open('/tmp/w2', 'w') as W2:
            print >>W1, w1
            print >>W2, w2
            W2.flush()
            W1.flush()
            try:
                r = subprocess.check_output('/Users/jhc/_Devel/evolwar/pmars-server /tmp/w1 /tmp/w2 -r %s 2>/dev/null|grep Results:' %rounds, shell=True)
            except:
                return 0, 0, 0
            else:
                a, b, c = map(int, r.strip().split()[1:])
                return a, b, c


def compete(w1, w2, generations):
    g = 0
    score = Counter()
    score[w1] += 0
    news = []
    while score:
        g += 1
        score = Counter(dict(score.most_common(20)))
        score.update(news)
        news = []
        for w in score.keys():            
            a, b, c = pmars(w, w2, 10)
            print a, b, c, len(score), g
            #raw_input()            
            if a + c > 0:
                score[w] = a
                ew = deepcopy(w)
                if evolve(ew):
                    news.append(ew)
            else:
                del score[w]
        
        print len(score)
        if g % 10 == 0:
            open('best', 'w').write(score.most_common(1)[0][0].export())
            open('orig', 'w').write(w2.export())
            print 'best:', [c2 for c1, c2 in score.most_common(20)]
            raw_input()
