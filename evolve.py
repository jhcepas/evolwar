from argparse import ArgumentParser

from cwevolver import mutate as mut
from cwevolver import redcode

# command line tool to evolve warriors...
def main(args):

    generations = 1000
    for warrior_file in args.warriors:
        warrior = redcode.parse(warrior_file)
        for i in xrange(generations):
            mut.evolver_1(warrior)
            
        for inst in warrior.instructions:
            print "%s.%s %s%s %s%s" %inst

            
if __name__ == '__main__':
    parser = ArgumentParser('Evolve corewar warrriors')
    parser.add_argument('warriors', metavar='warriors', type=str, nargs='+')                         
    args = parser.parse_args()    
    main(args)
