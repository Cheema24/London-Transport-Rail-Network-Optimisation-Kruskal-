#001364457-CHEEMA
import argparse
from pathlib import Path
from typing import List
from .task4a_simple_graph import tiny_dataset, dedupe_min_edge
from .task4a_mst_kruskal import mst_kruskal
from .task4b_experiments import time_mst_vs_n, save_runtime_plot
from .task4b_london_backbone import compute_backbone_report, load_edges_from_xlsx
from .impact_analysis import uses_redundant_edges
from .shortest_paths import dijkstra_path

def run_demo():
    edges = dedupe_min_edge(tiny_dataset())
    res = mst_kruskal(edges)
    print("DEMO (5-node)")
    print("MST total weight:", res.total_weight)
    print("MST edges:")
    for u, v, w in res.edges:
        print(f"  {u} -- {v}  {w}")
    print("Redundant edges:")
    for u, v, w in res.redundant_edges:
        print(f"  {u} -- {v}  {w}")

def run_experiments(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    points = time_mst_vs_n([50, 100, 200, 400, 800], trials=3)
    png = out_dir / "runtime_kruskal.png"
    save_runtime_plot(points, str(png))
    print("Runtime (ms):")
    for n, ms in points:
        print(f"  n={n}: {ms:.2f}")
    print("Saved plot:", png)

def run_london(xlsx_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    rep = compute_backbone_report(str(xlsx_path))
    print("LONDON BACKBONE")
    print("MST total weight:", rep.mst_total_weight)
    print("MST edges:")
    for u, v, w in rep.mst_edges:
        print(f"  {u} -- {v}  {w}")
    print("Sample redundant edges (>=10):")
    for u, v, w in rep.redundant_sample:
        print(f"  {u} -- {v}  {w}")

def run_impact_check(path_csv: str, xlsx_path: Path):
    path = [p.strip() for p in path_csv.split(",") if p.strip()]
    rep = compute_backbone_report(str(xlsx_path))
    flag = uses_redundant_edges(path, rep.mst_edges)
    print("IMPACT CHECK")
    print("Journey:", " -> ".join(path))
    print("Uses redundant edges:", flag)

def run_impact_analyze(xlsx_path: Path, start: str, end: str):
    full_edges = load_edges_from_xlsx(str(xlsx_path))
    rep = compute_backbone_report(str(xlsx_path))
    mst_edges = rep.mst_edges

    full_cost, full_path = dijkstra_path(full_edges, start, end)
    back_cost, back_path = dijkstra_path(mst_edges, start, end)

    mst_pairs = {tuple(sorted((u, v))) for (u, v, _) in mst_edges}
    def uses_redundant(path: List[str]) -> bool:
        return any(tuple(sorted((path[i], path[i+1]))) not in mst_pairs for i in range(len(path)-1))

    print("IMPACT ANALYSIS")
    print(f"Start: {start}    End: {end}")
    print()
    print("Original graph — shortest path:")
    print("  Path:", " -> ".join(full_path) if full_path else "(unreachable)")
    print("  Total time:", full_cost if full_cost != float('inf') else "∞")
    print("  Uses redundant edges:", uses_redundant(full_path) if full_path else "n/a")
    print()
    print("Backbone-only (MST) — shortest path:")
    print("  Path:", " -> ".join(back_path) if back_path else "(unreachable)")
    print("  Total time:", back_cost if back_cost != float('inf') else "∞")
    print()
    if full_cost != float("inf") and back_cost != float("inf"):
        diff = back_cost - full_cost
        print("Difference (backbone - original):", diff, "minutes")
        if diff > 0:
            print("Observation: Backbone removes shortcuts; journey is longer.")
        elif diff == 0:
            print("Observation: Journey unaffected by redundant closures.")
        else:
            print("Observation: Unexpected improvement on backbone (alternate low-cost tree route).")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",
        choices=["demo-5node", "experiments", "london-backbone", "impact-check", "impact-analyze"],
        required=True)
    parser.add_argument("--xlsx", default=str(Path(__file__).resolve().parents[1] / "data" / "London Underground data.xlsx"))
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[0] / "outputs"))
    parser.add_argument("--path", help='Comma-separated station list for impact-check, e.g. "A,B,C"')
    parser.add_argument("--start", help="Start station for impact-analyze")
    parser.add_argument("--end", help="End station for impact-analyze")
    args = parser.parse_args()

    if args.mode == "demo-5node":
        run_demo()
    elif args.mode == "experiments":
        run_experiments(Path(args.out))
    elif args.mode == "london-backbone":
        run_london(Path(args.xlsx), Path(args.out))
    elif args.mode == "impact-check":
        if not args.path:
            raise SystemExit('Please provide --path "Station1,Station2,...,StationN"')
        run_impact_check(args.path, Path(args.xlsx))
    elif args.mode == "impact-analyze":
        if not args.start or not args.end:
            raise SystemExit('Provide --start "A" --end "B"')
        run_impact_analyze(Path(args.xlsx), args.start, args.end)

if __name__ == "__main__":
    main()
