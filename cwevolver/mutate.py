import numpy as np
from collections import namedtuple
from random import randint, random, choice
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
    
def evolver_1(warrior):
    #mutator = np.array([0.01]*8)
    mutator = [0.005, 0.001, 0.001, 0.01, 0.01, 0.001, 0.001, 0.001]
    instructions = warrior.instructions
    
    # Duplications
    prob_duplication = mutator[0]
    dup_size_values = range(1, 10)
    dup_distance_values = range(1, 10)
    if random() < prob_duplication:
        dup_size = choice(dup_size_values)
        dup_dist = choice(dup_distance_values)        
        duplicate(instructions, dup_size, dup_dist)

    # Deletions
    prob_deletion = mutator[1]
    del_size = range(1, 10)    
    if random() < prob_deletion:
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
                values = position_values[i]
                inst[i] = choice(values)
        instructions[inst_index] = Instruction(*inst)

    return warrior
