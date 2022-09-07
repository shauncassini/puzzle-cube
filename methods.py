import utils
from typing import List, Dict, Set, Tuple

CubeMap = utils.CubeMap


def update_cube_map(holes: List[chr]):
    global CubeMap

    all_nodes = set(CubeMap)
    delete_nodes = all_nodes.difference(set(holes))

    for node in all_nodes:

        if node in delete_nodes:
            CubeMap.pop(node)
            continue

        check_nodes = set(CubeMap[node])
        for check_node in check_nodes:
            if check_node in delete_nodes:
                CubeMap[node].pop(check_node)


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


def transform(selection: Tuple[chr, ...], rotate: Tuple[int], flip: Tuple[int]) -> utils.Pieces:
    return []



if __name__ == '__main__':
    nodes = ['A', 'B', 'C', 'D', 'E', 'F']

    update_cube_map(nodes)
    graph = create_graph(nodes)
    cover = vertex_cover(graph)