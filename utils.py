from typing import List, Dict, Tuple, Union

# Depth and sides
T, R, B, L = 0, 1, 2, 3
D0, D1, D2 = 0, 1, 2

CubeMapType = Dict[chr, Dict[chr, Tuple[int, int]]]
PiecesType = Dict[int, Dict[int, Tuple[float, float, float]]]

# From Hole -> To hole ->
# (Side, Depth)
CubeMap: CubeMapType = {
    'A': {
        'E': (B, D0),
        'F': (B, D2),
        'G': (R, D1),
    },
    'B': {
        'E': (B, D0),
        'F': (B, D2),
        'G': (L, D1),
    },
    'C': {
        'E': (T, D0),
        'F': (T, D2),
        'G': (R, D1),
    },
    'D': {
        'E': (T, D0),
        'F': (T, D2),
        'G': (L, D1),
    },
    'E': {
        'A': (T, D2),
        'B': (T, D0),
        'C': (B, D2),
        'D': (B, D0),
        'G': (R, D1),
    },
    'F': {
        'A': (T, D2),
        'B': (T, D0),
        'C': (B, D2),
        'D': (B, D0),
        'G': (L, D1),
    },
    'G': {
        'A': (T, D2),
        'B': (L, D0),
        'C': (T, D0),
        'D': (L, D2),
        'E': (R, D1),
        'F': (L, D1),
    }
}

CubeValues = {
    from_node: {to_node: 0 for to_node in CubeMap[from_node]} for from_node in CubeMap
}

# Piece number -> side -> depths (0, 1, 2)
Pieces: PiecesType = {x: {T: (), R: (), B: (), L: ()} for x in range(1, 18)}

# Set up pieces from csv
with open('pieces.csv') as f:
    # Ignore header
    f.readline()
    # File is in format piece num, Depth n, T R B L for n in (1, 2, 3)
    pieces_str: List[str] = f.read().splitlines()
    for i, piece in enumerate(pieces_str):
        ps = piece.split(',')[1:]
        ps_ = [p.split() for p in ps]
        # rotation
        for r in range(4):
            # assign depths
            d0, d1, d2 = float(ps_[0][r]), float(ps_[1][r]), float(ps_[2][r])
            Pieces[i+1][r] = (d0, d1, d2)

    f.close()


def get_edge(a: chr, b: chr) -> Union[Tuple[int, int], bool]:
    try:
        first_node = CubeMap[a]
    except KeyError:
        print(f'Invalid hole: {a}')
        return False
    try:
        return first_node[b]
    except KeyError:
        if b not in CubeMap:
            print(f'Invalid hole: {b}')
        else:
            print(f'No edge between {a} and {b}')
        return False


def get_piece(p: int) -> Dict[int, Tuple[float, float, float]]:
    try:
        return Pieces[p]
    except KeyError:
        print(f'Invalid piece: {p}')
