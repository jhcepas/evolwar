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
    "Return the scores of competing warriors w1 and w2"
    with tempfile.NamedTemporaryFile(dir='/tmp') as f1:
        f1.write(str(w1))
        f1.flush()
        with tempfile.NamedTemporaryFile(dir='/tmp') as f2:
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
    mutants = 0
    populations = [[ (0, w1) ]] * 5
    min_fitness = 0
    max_fitness = 0
    for expected_fitness in [10, 100]:
        while max_fitness < expected_fitness:
            g += 1
            # Generate new warriors from the top 20 parents
            evolved = []
            for pop in populations:
                for fitness, w in pop:
                    if fitness < expected_fitness:
                        for _ in xrange(1):
                            new = deepcopy(w)
                            evolve(new)
                            evolved.append((new, pop))

            # Evaluate new warriors
            new_mutant = 0
            for w, pop in evolved:
                mutants += 1
                new_mutant += 1
                a, b, c = pmars(w, w2, expected_fitness, './pmars-server')
                print '% 3s % 3s % 3s   score:% 3d /% 3d   mutants:% 7d   generarion:% 3d /% 3d' %\
                    (a, b, c, max_fitness, expected_fitness, mutants, new_mutant, len(evolved))

                # If warrior won at least a battle, keep it 
                if a + c > 0:
                    if a > min_fitness: 
                        pop.append((a, w))

            populations = [sorted(pop, reverse=True)[:20] for pop in populations]
            populations.sort(reverse=True)
            min_fitness = populations[0][-1][0]
            max_fitness = populations[0][0][0]

            if g % 10 == 0:
                open('best', 'w').write(populations[0][0][1].export())
                open('orig', 'w').write(w2.export())
                print 'best:', [fit for fit, w in pop for pop in populations]
                raw_input()
        raw_input()

        open('best', 'w').write(populations[0][0][1].export())
        open('orig', 'w').write(w2.export())
        print 'best:', [fit for fit, w in pop for pop in populations]
