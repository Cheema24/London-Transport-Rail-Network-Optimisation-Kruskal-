#001364457-CHEEMA
import random, time
from typing import List, Tuple
from .task4a_mst_kruskal import mst_kruskal, Edge

def gnp_weighted(n: int, p: float, w_low: int = 1, w_high: int = 20) -> List[Edge]:
    nodes = [f"v{i}" for i in range(n)]
    edges: List[Edge] = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                edges.append((nodes[i], nodes[j], random.randint(w_low, w_high)))
    if not edges:
        for i in range(n - 1):
            edges.append((nodes[i], nodes[i + 1], random.randint(w_low, w_high)))
    return edges

def time_mst_vs_n(ns: List[int], trials: int = 5) -> List[Tuple[int, float]]:
    out = []
    for n in ns:
        t = 0.0
        for _ in range(trials):
            edges = gnp_weighted(n, p=min(0.02 * (50 / max(5, n)), 0.1))
            s = time.perf_counter()
            mst_kruskal(edges)
            t += time.perf_counter() - s
        out.append((n, (t / trials) * 1000.0))
    return out

def save_runtime_plot(points: List[Tuple[int, float]], out_png: str):
    import matplotlib.pyplot as plt
    xs = [n for n, _ in points]
    ys = [ms for _, ms in points]
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.xlabel("n (nodes)")
    plt.ylabel("avg time (ms)")
    plt.title("Kruskal runtime vs n")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()
