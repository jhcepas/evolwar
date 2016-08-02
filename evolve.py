#!/usr/bin/env python

from argparse import ArgumentParser

from cwevolver import mutate as mut
from cwevolver import redcode

def main(args):

    generations = 1000
    for warrior_file in args.warriors:
        w1 = redcode.parse(warrior_file)
        w2 = redcode.parse(warrior_file)
        
        mut.compete(w1, w2, args.generations)

        print w1
        print
        print w2

            
if __name__ == '__main__':
    parser = ArgumentParser('Evolve corewar warrriors')
    parser.add_argument('warriors', metavar='warriors', type=str, nargs='+')
    parser.add_argument('-g', dest='generations', type=int, default=10)
    
    args = parser.parse_args()    
    main(args)
