#001364457-CHEEMA
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Dict

Edge = Tuple[str, str, int]

def _add_paths():
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / "clrsPython"
    if root.exists():
        for p in [root, *root.rglob("*")]:
            if p.is_dir():
                sp = str(p)
                if sp not in sys.path:
                    sys.path.append(sp)
_add_paths()

from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal

@dataclass
class MSTResult:
    total_weight: int
    edges: List[Edge]
    redundant_edges: List[Edge]

def _index_map(edges: Iterable[Edge]) -> Dict[str, int]:
    names = set()
    for u, v, _ in edges:
        names.add(u); names.add(v)
    return {name: i for i, name in enumerate(sorted(names))}

def _build_graph(idx: Dict[str, int], edges: Iterable[Edge]):
    G = AdjacencyListGraph(len(idx), False, True)
    for u, v, w in edges:
        G.insert_edge(idx[u], idx[v], int(w))
    return G

def _k(u: str, v: str) -> Tuple[str, str]:
    return tuple(sorted((u, v)))

def mst_kruskal(edges: Iterable[Edge]) -> MSTResult:
    edges = list(edges)
    idx = _index_map(edges)
    ridx = {i: n for n, i in idx.items()}
    G = _build_graph(idx, edges)
    mst_graph = kruskal(G)

    mst_pairs = set()
    mst_list: List[Edge] = []
    total = 0
    for u in range(mst_graph.get_card_V()):
        for e in mst_graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                a, b = ridx[u], ridx[v]
                w = int(e.get_weight())
                mst_list.append((a, b, w))
                mst_pairs.add(_k(a, b))
                total += w

    original_pairs = {}
    for a, b, w in edges:
        k = _k(a, b)
        if k not in original_pairs or w < original_pairs[k][2]:
            original_pairs[k] = (a, b, int(w))
    redundant = [v for k, v in original_pairs.items() if k not in mst_pairs]

    mst_list.sort(key=lambda x: (x[2], x[0], x[1]))
    redundant.sort(key=lambda x: (x[2], x[0], x[1]))
    return MSTResult(total_weight=total, edges=mst_list, redundant_edges=redundant)
#001364457-CHEEMA