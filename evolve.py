from argparse import ArgumentParser

from cwevolver import mutate as mut

# command line tool to evolve warriors...
def main(args):
    for warrior_file in args.warriors:
        mut.mut_1(open(warrior_file).readlines())

if __name__ == '__main__':
    parser = ArgumentParser('Evolve corewar warrriors')
    parser.add_argument('warriors', metavar='warriors', type=str, nargs='+')                         
    args = parser.parse_args()    
    main(args)
