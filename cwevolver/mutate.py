import numpy as np
from subprocess import check_output
from collections import namedtuple
from random import randint, random, choice
from copy import deepcopy
from collections import defaultdict, Counter
import tempfile
import os

from redcode import parse, OPCODES, MODIFIERS, MODES, Instruction


def duplicate(instructions, dup_size, dup_dist):
    "Insert in-place a duplication of size dup_size after at max dup_dist"
    start = randint(0, len(instructions))
    end = randint(start+1, start+dup_size+1)
    insert_point = randint(start+1, start+dup_dist)
    instructions[insert_point:insert_point] = instructions[start:end]

def delete(instructions, loss_size):
    "Delete in-place at max loss_size instructions"
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


def pmars(w1, w2, rounds, pmars_server='pmars-server'):
    pmars_server='../pmars-0.9.2/src/pmars'):
    "Return the scores of competing warriors w1 and w2"
    with tempfile.NamedTemporaryFile(dir='/dev/shm') as f1:
        f1.write(str(w1))
        f1.flush()
        with tempfile.NamedTemporaryFile(dir='/dev/shm') as f2:
            f2.write(str(w2))
            f2.flush()
            try:
                r = check_output([pmars_server, f1.name, f2.name,
                                  '-r', str(rounds)], stderr=open(os.devnull))
            except Exception:
                return 0, 0, 0

            for line in r.splitlines():
                if line.startswith('Results:'):
                    return [int(x) for x in line.strip().split()[1:]]


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
            a, b, c = pmars(w, w2, 100)
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
