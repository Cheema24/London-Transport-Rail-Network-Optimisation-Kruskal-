#001364457-CHEEMA
from typing import Dict, List, Tuple
import heapq

Edge = Tuple[str, str, int]

def _build_adj(edges: List[Edge]) -> Dict[str, List[Tuple[str, int]]]:
    adj: Dict[str, List[Tuple[str, int]]] = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj

def dijkstra_path(edges: List[Edge], start: str, end: str) -> Tuple[int, List[str]]:
    start_n = start.strip()
    end_n = end.strip()
    adj = _build_adj(edges)
    dist: Dict[str, int] = {start_n: 0}
    prev: Dict[str, str] = {}
    pq = [(0, start_n)]
    seen = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == end_n:
            break
        for v, w in adj.get(u, []):
            nd = d + int(w)
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if end_n not in dist:
        return (float("inf"), [])

    path: List[str] = []
    cur = end_n
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.append(start_n)
    path.reverse()
    return (dist[end_n], path)
#001364457-CHEEMA