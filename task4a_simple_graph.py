#001364457-CHEEMA
from typing import List, Tuple

Edge = Tuple[str, str, int]

def tiny_dataset() -> List[Edge]:
    return [
        ("A", "C", 2),
        ("C", "D", 3),
        ("A", "B", 4),
        ("B", "C", 5),
        ("D", "E", 6),
        ("C", "E", 7),
        ("A", "E", 8),
        ("B", "E", 9),
        ("A", "D", 10),
        ("B", "D", 10),
    ]

def dedupe_min_edge(edges: List[Edge]) -> List[Edge]:
    best = {}
    for u, v, w in edges:
        a, b = sorted((u, v))
        k = (a, b)
        if k not in best or w < best[k]:
            best[k] = w
    return [(a, b, w) for (a, b), w in best.items()]
