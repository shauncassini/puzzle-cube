import argparse
import itertools
from utils import get_piece
import methods
import random

parser = argparse.ArgumentParser(description='Solve The Sherlock')
parser.add_argument('--holes', type=str, nargs='+', help='the holes for the pegs')
parser.add_argument('--pegs', type=int, nargs='+', help='the pegs for the holes')

args = parser.parse_args()


def check_args(pegs, holes):

    if len(pegs) != len(holes):
        exit(f'Number of pegs ({len(pegs)}) must be same as number of holes ({len(holes)})')

    if len(set(holes)) != len(holes):
        exit('No duplicate holes')

    for peg in set(pegs):
        if peg < 1 or peg > 17:
            exit('Pegs must be in the range (1, 17)')

    for hole in holes:
        if hole < 'A' or hole > 'G':
            exit('Holes must be in the range (A, G)')

    print('Arguments are valid')


pegs, holes = args.pegs, args.holes

check_args(pegs, holes)

# Update CubeMap
methods.update_cube_map(holes)

# Create vertex cover of graph
graph = methods.create_graph(holes)
cover = methods.vertex_cover(graph)

# Shuffle the pegs
random.shuffle(pegs)

# unique permutations of pegs for cover (set(pegs) is unique)
selections = itertools.permutations(set(pegs), len(cover))

# all transformations for each peg in the cover
rotations = itertools.product(*([range(4)] * len(cover)))
flips = itertools.product(*([range(2)] * len(cover)))
transformations = list(itertools.product(list(rotations), list(flips)))

""" Main algorithm 

1. Iterate through each permutation of pegs to satisfy vertex cover.
2. Once the vertex cover is satisfied, compute the target pegs for the
   remaining holes. If not successful, repeat step 1.
   
Computing the vertex cover decreases the num. of permutations 
from n! * 4^n * 2^n to n * (n-1) * ... * (n-k) * 4^k * 2^k
where n is the number of pegs and k is the size of the vertex cover

"""

match_found = False
while not match_found:
    try:
        # use iterator, so you can always carry on where you left off
        selection = next(selections)
    except StopIteration:
        break

    # put pegs in cover, evaluate
    for transform in transformations:
        # rotations and flips for each peg
        rotation, flip = transform
        transformed_pegs = methods.transform(selection, rotation, flip)
        # check if pegs fit in cover, search for remaining nodes
        if methods.evaluate(cover, transformed_pegs) < 1:
            target_pegs = methods.get_targets(cover, transformed_pegs, pegs)
            matches, match_transforms = methods.get_matches(target_pegs, pegs)
            if matches:
                print('solution found!')
                match_found = True
