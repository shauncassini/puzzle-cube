import utils
from typing import List, Dict, Set, Tuple

CubeMap = utils.CubeMap
CubeValues = utils.CubeValues


def update_cube_map(holes: List[chr]):
    global CubeMap, CubeValues

    all_nodes = set(CubeMap)
    delete_nodes = all_nodes.difference(set(holes))

    for node in all_nodes:

        if node in delete_nodes:
            CubeMap.pop(node)
            CubeValues.pop(node)
            continue

        check_nodes = set(CubeMap[node])
        for check_node in check_nodes:
            if check_node in delete_nodes:
                CubeMap[node].pop(check_node)
                CubeValues[node].pop(check_node)


def create_graph(holes: List[chr]) -> Dict[chr, List[chr]]:
    graph = {}
    for h in holes:
        graph[h] = list(CubeMap[h].keys())
    return graph


def vertex_cover(graph: Dict[chr, List[chr]]) -> List[chr]:
    cover = []

    # Start at vertices with most edges
    graph_sizes = {n: len(v) for n, v in graph.items()}
    sorted_nodes = sorted(graph_sizes.items(), reverse=True)

    visited = {n: False for n in graph.keys()}

    for u, _ in sorted_nodes:
        if not visited[u]:
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    visited[u] = True
                    cover.append(u)
                    break

    return cover


def apply_transform(node, transform_r, transform_f):
    r, f = node

    # rotating is modular arithmetic
    r_t = (r + transform_r) % 4

    # flipping swaps depth 0 and 2
    f_t = f
    if f == 0 and transform_f == 1:
        f_t = 2
    elif f == 2 and transform_f == 1:
        f_t = 0

    return r_t, f_t


def evaluate(nodes: List[chr], pegs: Tuple[chr, ...], transforms: Tuple[Tuple[int, ...], Tuple[int, ...]]):

    # empty cube values (because it is constantly being referenced to)
    # slightly better than deepcopy, as it only accesses the necessary nodes
    cv = CubeValues
    for from_n in nodes:
        for to_n in cv[from_n]:
            cv[from_n][to_n] = 0

    # each peg has a transform
    rotations, flips = transforms
    # compute intersections
    intersection = False

    for i in range(len(nodes)):

        if intersection:
            break

        from_node = nodes[i]
        peg = utils.get_piece(pegs[i])

        rotation = rotations[i]
        flip = flips[i]

        to_nodes = CubeMap[from_node]
        for to_node in to_nodes:

            # Set value of edge to value of peg at that location
            from_e = to_nodes[to_node]
            peg_rotation, peg_flip = apply_transform(from_e, rotation, flip)
            from_value = peg[peg_rotation][peg_flip]
            cv[from_node][to_node] = from_value

            # from_node and to_node are both in the vertex cover, check for intersection
            to_value = cv[to_node][from_node]
            clash = from_value + to_value
            if clash > 1:
                intersection = True
                break

    return intersection, cv


def clear_nones(target_peg: List[List[any]]) -> Dict[int, Dict[int, int]]:
    peg = dict(dict())
    for i in range(4):
        for j in range(3):
            if not target_peg[i][j]:
                continue
            depths = peg.get(i, {})
            depths[j] = target_peg[i][j]
            peg.update({i: depths})

    return peg


def get_targets(nodes, cube_values):
    # returns a list of target pegs based on the inverse of each occupied node
    target_pegs = []
    half_cut_piece = False
    for from_node in nodes:
        # 2 target pegs in case we encounter half_cut_piece

        target_peg1 = [[None for _ in range(3)] for _ in range(4)]
        target_peg2 = [[None for _ in range(3)] for _ in range(4)]

        for to_node in cube_values[from_node]:
            # ignores already solved interactions
            if cube_values[from_node][to_node] == 0:

                target = -cube_values[to_node][from_node]

                side = CubeMap[from_node][to_node][0]
                depth = CubeMap[from_node][to_node][1]

                # In this case, we are dealing with a half-cut piece (piece 16 or 17)
                # several targets must be made in this annoying case: -1 or 0.5
                if target == 0:
                    # now every change that is done to the target peg is to be duplicated
                    half_cut_piece = True
                    target_peg1[side][depth] = -1
                    target_peg2[side][depth] = 0.5
                else:
                    target_peg1[side][depth] = target

                if half_cut_piece and target != 0:
                    target_peg1[side][depth] = target
                    target_peg2[side][depth] = target

        # Remove None before appending and convert to dict
        target_peg1 = clear_nones(target_peg1)
        target_pegs.append(target_peg1)

        if half_cut_piece:
            target_peg2 = clear_nones(target_peg2)
            target_pegs.append(target_peg2)
            half_cut_piece = False

    return target_pegs


if __name__ == '__main__':
    nds = ['A', 'B', 'C', 'D', 'E', 'F']

    update_cube_map(nds)
    g = create_graph(nds)
    c = vertex_cover(g)
