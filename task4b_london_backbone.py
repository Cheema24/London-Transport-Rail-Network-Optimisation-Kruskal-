#001364457-CHEEMA
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd
from .task4a_simple_graph import dedupe_min_edge
from .task4a_mst_kruskal import mst_kruskal, Edge

@dataclass
class BackboneReport:
    mst_total_weight: int
    mst_edges: List[Edge]
    redundant_sample: List[Edge]

def _detect_columns(df: pd.DataFrame):
    cols = list(df.columns)
    cand = {
        "u": ["From", "Station A", "Source", "Origin", "u"],
        "v": ["To", "Station B", "Target", "Destination", "v"],
        "w": ["Time", "Minutes", "Weight", "Duration", "time", "minutes", "weight"],
    }
    def pick(names):
        for n in names:
            if n in cols:
                return n
    cu, cv, cw = pick(cand["u"]), pick(cand["v"]), pick(cand["w"])
    if cu and cv and cw:
        return cu, cv, cw
    nonnum = [c for c in cols if not pd.api.types.is_numeric_dtype(df[c])]
    num = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    if len(nonnum) >= 2 and len(num) >= 1:
        return nonnum[0], nonnum[1], num[0]
    raise ValueError("Cannot detect From/To/Time columns.")

def load_edges_from_xlsx(path: str) -> List[Edge]:
    import math
    df = pd.read_excel(path)
    cu, cv, cw = _detect_columns(df)
    rows = df[[cu, cv, cw]].dropna()

    def norm_station(x: object) -> str:
        return str(x).strip()

    edges_raw: List[Edge] = []
    for _, r in rows.iterrows():
        u = norm_station(r[cu])
        v = norm_station(r[cv])
        try:
            w = int(round(float(r[cw])))
        except Exception:
            continue
        if not u or not v:
            continue
        if u.casefold() == v.casefold():
            continue
        if w <= 0 or math.isinf(w):
            continue
        edges_raw.append((u, v, w))

    return dedupe_min_edge(edges_raw)

def compute_backbone_report(xlsx_path: str) -> BackboneReport:
    edges = load_edges_from_xlsx(xlsx_path)
    res = mst_kruskal(edges)
    sample = res.redundant_edges[: max(10, min(25, len(res.redundant_edges)))]
    return BackboneReport(res.total_weight, res.edges, sample)
