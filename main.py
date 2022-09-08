import argparse
import itertools
from utils import get_piece
import methods
import random

parser = argparse.ArgumentParser(description='Solve The Sherlock')
parser.add_argument('--holes', type=str, nargs='+', help='the holes for the input_pegs')
parser.add_argument('--pegs', type=int, nargs='+', help='the input_pegs for the holes')

args = parser.parse_args()


def check_args(pegs, holes):

    if len(pegs) != len(holes):
        exit(f'Number of input_pegs ({len(pegs)}) must be same as number of holes ({len(holes)})')

    if len(set(holes)) != len(holes):
        exit('No duplicate holes')

    for peg in set(pegs):
        if peg < 1 or peg > 17:
            exit('Pegs must be in the range (1, 17)')

    for hole in holes:
        if hole < 'A' or hole > 'G':
            exit('Holes must be in the range (A, G)')

    print('Arguments are valid')


input_pegs, holes = args.pegs, args.holes

check_args(input_pegs, holes)

# Update CubeMap
methods.update_cube_map(holes)

# Create vertex cover of graph
graph = methods.create_graph(holes)
cover = methods.vertex_cover(graph)
difference = list(set(holes) - set(cover))

# Shuffle the input_pegs
random.shuffle(input_pegs)

# permutations of input_pegs for cover
selections = itertools.permutations(input_pegs, len(cover))

# all transformations for each peg in the cover
rotations = itertools.product(*([range(4)] * len(cover)))
flips = itertools.product(*([range(2)] * len(cover)))
transforms = list(itertools.product(list(rotations), list(flips)))

""" Main algorithm 

1. Iterate through each permutation of input_pegs to satisfy vertex cover.
2. Once the vertex cover is satisfied, compute the target input_pegs for the
   remaining holes. If not successful, repeat step 1.
   
Computing the vertex cover decreases the num. of permutations 
from n! * 4^n * 2^n to n * (n-1) * ... * (n-k) * 4^k * 2^k
where n is the number of input_pegs and k is the size of the vertex cover

"""

match_found = False
# while not match_found:
c, m = 0, 0
while not match_found:
    try:
        # use iterator, so you can always carry on where you left off
        cover_pegs = next(selections)
    except StopIteration:
        break

    # put input_pegs in cover, evaluate
    for transform in transforms:
        # check if input_pegs fit in cover, search for remaining nodes
        intersection, cube_values = methods.evaluate(cover, cover_pegs, transform)
        c += 1
        if not intersection:
            m += 1
            target_pegs = methods.get_targets(difference, cube_values)
        #     match_pegs, match_transforms = methods.get_matches(target_pegs, input_pegs)
        #     if match_pegs:
        #         print('solution found!')
        #         match_found = True

print(c, m)
