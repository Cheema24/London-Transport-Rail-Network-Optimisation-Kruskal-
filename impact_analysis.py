#001364457-CHEEMA
from typing import List, Tuple

Edge = Tuple[str, str, int]

def uses_redundant_edges(path: List[str], mst_edges: List[Edge]) -> bool:
    norm = lambda s: str(s).strip().casefold()
    mst_pairs = {tuple(sorted((norm(u), norm(v)))) for (u, v, _) in mst_edges}
    for i in range(len(path) - 1):
        a, b = norm(path[i]), norm(path[i + 1])
        if tuple(sorted((a, b))) not in mst_pairs:
            return True
    return False
#001364457-CHEEMA