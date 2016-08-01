from collections import namedtuple
from copy import copy
import re


INSTRUCTION_REGEX = re.compile(
    r'([a-z]{3})'  # opcode
    r'(?:\s*\.\s*([abfxi]{1,2}))?' # optional modifier
    r'(?:\s*([#\$\*@\{<\}>])?\s*([^,$]+))?' # optional first value
    r'(?:\s*,\s*([#\$\*@\{<\}>])?\s*(.+))?$', # optional second value
    re.I)


OPCODES = ['DAT', 'MOV', 'ADD', 'SUB', 'MUL',
           'DIV', 'MOD', 'JMP', 'JMZ', 'JMN',
           'DJN', 'SPL', 'SLT', 'CMP', 'SEQ',
           'SNE', 'NOP']
# DAT: terminate process
# MOV: move from A to B
# ADD: add A to B, store result in B
# SUB: subtract A from B, store result in B
# MUL: multiply A by B, store result in B
# DIV: divide B by A, store result in B if A <> 0, else terminate
# MOD: divide B by A, store remainder in B if A <> 0, else terminate
# JMP: transfer execution to A
# JMZ: transfer execution to A if B is zero
# JMN: transfer execution to A if B is non-zero
# DJN: decrement B, if B is non-zero, transfer execution to A
# SPL: split off process to A
# SLT: skip next instruction if A is less than B
# CMP: same as SEQ
# SEQ: Skip next instruction if A is equal to B
# SNE: Skip next instruction if A is not equal to B
# NOP: No operation

MODIFIERS = ['A', 'B', 'AB', 'BA', 'F', 'X', 'I']
# A:  Instructions read and write A-fields.
# B:  Instructions read and write B-fields.
# AB: Instructions read the A-field of the A-instruction and the
#     B-field of the B-instruction and write to B-fields.
# BA: Instructions read the B-field of the A-instruction and the
#     A-field of the B-instruction and write to A-fields.
# F:  Instructions read both A- and B-fields of the A and B-instruction
#     and write to both A- and B-fields (A to A and B to B).
# X:  Instructions read both A- and B-fields of the A and B-instruction
#     and write to both A- and B-fields exchanging fields (A to B and
#     B to A).
# I:  Instructions read and write entire instructions.


MODES = ['#', '$', '@', '<', '>', '*', '{', '}']
# IMMEDIATE: immediate
# DIRECT: direct
# INDIRECT_B: indirect using B-field
# PREDEC_B : predecrement indirect using B-field
# POSTINC_B: postincrement indirect using B-field
# INDIRECT_A: indirect using A-field
# PREDEC_A: predecrement indirect using A-field
# POSTINC_A: postincrement indirect using A-field


class Warrior(object):
    "A Redcode Warrior, with instructions and meta-data"

    def __init__(self, name='Unnamed', author='Anonymous', date=None,
                 version=None, strategy=None, start=0):
        self.name = name
        self.author = author
        self.date = date
        self.version = version
        self.strategy = strategy or []
        self.start = start
        self.instructions = []

    def __iter__(self):
        return iter(self.instructions)

    def __len__(self):
        return len(self.instructions)

    def __repr__(self):
        return "<Warrior name=%s %d instructions>" % (self.name,
                                                      len(self.instructions))

    def export(self):
        lines = ["ORG %s" %self.start]
        for i in self.instructions:
            cmd = "%s.%s %s%s, %s%s" %i
            
            lines.append(cmd.upper())
        lines.append('END')
        
        return '\n'.join(lines)

    def __str__(self):
        lines = ["ORG %s" %self.start]
        for i in self.instructions:
            cmd = "%s.%s %s%s, %s%s" %i
            
            lines.append(cmd.upper())
        lines.append('END')
        
        return '\n'.join(lines)

    
        
Instruction = namedtuple('Instruction',
                         'opcode modifier a_mode a_number b_mode b_number')


def parse(fname, definitions={}):
    "Return a warrior parsed from file fname"

    found_recode_info_comment = False
    labels = {}
    code_address = 0

    warrior = Warrior()

    # use a version of environment because we're going to add names to it
    environment = copy(definitions)

    # first pass
    for n, line in enumerate(open(fname)):
        line = line.strip()
        if line:
            # process info comments
            m = re.match(r'^;redcode\w*$', line, re.I)
            if m:
                if found_recode_info_comment:
                    # stop reading, found second ;redcode
                    break;
                else:
                    # first ;redcode ignore all input before
                    warrior.instructions = []
                    labels = {}
                    environment = copy(definitions)
                    code_address = 0
                    found_recode_info_comment = True
                continue

            m = re.match(r'^;name\s+(.+)$', line, re.I)
            if m:
                warrior.name = m.group(1).strip()
                continue

            m = re.match(r'^;author\s+(.+)$', line, re.I)
            if m:
                warrior.author = m.group(1).strip()
                continue

            m = re.match(r'^;date\s+(.+)$', line, re.I)
            if m:
                warrior.date = m.group(1).strip()
                continue

            m = re.match(r'^;version\s+(.+)$', line, re.I)
            if m:
                warrior.version = m.group(1).strip()
                continue

            m = re.match(r'^;strat(?:egy)?\s+(.+)$', line, re.I)
            if m:
                warrior.strategy.append(m.group(1).strip())
                continue

            # Test if assert expression evaluates to true
            m = re.match(r'^;assert\s+(.+)$', line, re.I)
            if m:
                if not eval(m.group(1), environment):
                    raise AssertionError("Assertion failed: %s, line %d" % (line, n))
                continue

            # ignore other comments
            m = re.match(r'^([^;]*)\s*;', line)
            if m:
                # rip off comment from the line
                line = m.group(1).strip()
                # if this is a comment line
                if not line: continue

            # Match ORG
            m = re.match(r'^ORG\s+(.+)\s*$', line, re.I)
            if m:
                warrior.start = m.group(1)
                continue

            # Match END
            m = re.match(r'^END(?:\s+([^\s]+))?$', line, re.I)
            if m:
                if m.group(1):
                    warrior.start = m.group(1)
                break # stop processing (end of redcode)

            # Match EQU
            m = re.match(r'^([a-z]\w*)\s+EQU\s+(.*)\s*$', line, re.I)
            if m:
                name, value = m.groups()
                # evaluate EQU expression using previous EQU definitions,
                # add result to a name variable in environment
                environment[name] = eval(value, environment)
                continue

            # Keep matching the first word until it's no label anymore
            while True:
                m = re.match(r'^([a-z]\w*)\s+(.+)\s*$', line)
                if m:
                    label_candidate = m.group(1)
                    if label_candidate.upper() not in OPCODES:
                        labels[label_candidate] = code_address

                        # strip label off and keep looking
                        line = m.group(2)
                        continue
                # its an instruction, not label. proceed OR no match, probably
                # a all-value-omitted instruction.
                break

            # At last, it should match an instruction
            m = INSTRUCTION_REGEX.match(line)
            if not m:
                raise ValueError('Error at line %d: expected instruction in expression: "%s"' %
                                 (n, line))
            else:
                opcode, modifier, a_mode, a_number, b_mode, b_number = m.groups()

                if opcode.upper() not in OPCODES:
                    raise ValueError('Invalid opcode: %s in line %d: "%s"' %
                                     (opcode, n, line))
                if modifier is not None and modifier.upper() not in MODIFIERS:
                    raise ValueError('Invalid modifier: %s in line %d: "%s"' %
                                     (modifier, n, line))

                # add parts of instruction read. the fields should be parsed
                # as an expression in the second pass, to expand labels
                warrior.instructions.append(Instruction(opcode, modifier.upper(),
                                                        a_mode, a_number,
                                                        b_mode, b_number))

            # increment code counting
            code_address += 1

    # join strategy lines with line breaks
    warrior.strategy = '\n'.join(warrior.strategy)

    # evaluate start expression
    if isinstance(warrior.start, str):
        warrior.start = eval(warrior.start, environment, labels)

    # second pass
    for n, instruction in enumerate(warrior.instructions):

        # create a dictionary of relative labels addresses to be used as a local
        # eval environment
        relative_labels = dict((name, address-n) for name, address in labels.iteritems())

        # evaluate instruction fields using global environment and labels
        if isinstance(instruction.a_number, str):
            instr = list(instruction)
            instr[3] = eval(instruction.a_number, environment, relative_labels)
            instruction = Instruction(*instr)
            warrior.instructions[n] = instruction
        if isinstance(instruction.b_number, str):
            instr = list(instruction)
            instr[5] = eval(instruction.b_number, environment, relative_labels)
            instruction = Instruction(*instr)
            warrior.instructions[n] = instruction

    return warrior
