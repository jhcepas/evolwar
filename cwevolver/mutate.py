from collections import namedtuple
from random import randint, random, choice
from redcode import parse, OPCODES, MODIFIERS, MODES, Instruction

def duplicate(warrior, dup_size, dup_dist):
    start = randint(0, len(warrior))
    end = randint(start+1, start+dup_size+1)
    insert_point = randint(start+1, start+dup_dist)
    warrior[insert_point:insert_point] = warrior[start:end]

def delete(warrior, loss_size):
    start = randint(0, len(warrior))
    end = randint(start+1, start+loss_size+1)
    warrior[start:end] = []
    
def evolver_1(w):
    warrior = parse(w)
    instructions = warrior.instructions
    
    # Duplications
    prob_duplication = 0.01
    dup_size_values = range(1, 10)
    dup_distance_values = range(1, 10)
    if random() < prob_duplication:
        dup_size = choice(dup_size_values)
        dup_distance = choice(dup_distance_values)        
        duplicate(instructions, dup_size, dup_dist)

    # Deletions
    prob_deletion = 0.01
    del_size = range(1, 10)    
    if random() < prob_deletion:
        dup_size = choice(dup_size_values)
        dup_distance = choice(dup_distance_values)        
        delete(instructions, dup_size, dup_dist)

    # Point mutations
    position_values = {
        0: OPCODES,
        1: MODIFIERS,
        2: MODES,
        3: range(-10, 10),
        4: MODES,
        5: range(-10, 10),
    }
    inst_index = randint(0, len(instructions)-1)
    prob_mutation = [0.9, 0.01, 0.01, 0.01, 0.01, 0.01]
    inst = list(instructions[inst_index])
    for i, mut_rate in enumerate(prob_mutation):
        if random() < mut_rate:
            values = position_values[i]
            inst[i] = choice(values)
    instructions[inst_index] = Instruction(*inst)    
    print warrior.instructions
    return warrior



        


