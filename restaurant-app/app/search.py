"""
CLI Search & AI Query Tool for Isarva Restaurant POS.
Usage:
  python search.py "how to split bill"
  python search.py --troubleshoot "tax looks wrong"
  python search.py --role "Food Server" "merge tables"
  python search.py --module "Settle" "mada card"
  python search.py --ai-context "how to perform day close"
  python search.py --benchmark
"""
import argparse
import os
import sys
import time
import orjson

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from src.search_engine import POSSearchEngine
from src.ai_indexer import build_ai_index

def run_benchmark(engine: POSSearchEngine, iterations: int = 500):
    queries = [
        "how to split bill",
        "activate pos company code",
        "send kot to kitchen",
        "change table merge table",
        "tax looks wrong on bill",
        "food voucher discount",
        "day close cash drawer count",
        "hungerstation jahez delivery",
        "kitchen screen kds bump item",
        "stock receiving purchase order"
    ]
    print(f"\n[BENCHMARK] Running {iterations} search iterations across {len(queries)} queries...")
    t0 = time.perf_counter()
    total_queries = 0
    for _ in range(iterations // len(queries)):
        for q in queries:
            engine.search(q, top_k=3)
            total_queries += 1
    total_time_ms = (time.perf_counter() - t0) * 1000
    avg_latency_ms = total_time_ms / total_queries
    qps = total_queries / (total_time_ms / 1000)
    print(f"[RESULTS] Executed {total_queries} searches in {total_time_ms:.1f}ms")
    print(f" -> Average latency: {avg_latency_ms:.3f}ms per query")
    print(f" -> Throughput: {qps:,.1f} Queries/Second")

def main():
    parser = argparse.ArgumentParser(description="Isarva Restaurant POS Ultra-Fast AI Search Engine")
    parser.add_argument("query", nargs="?", default=None, help="Search query string")
    parser.add_argument("--role", type=str, default=None, help="Filter by role (Admin, Cashier, Food Server, Kitchen Manager, Rider)")
    parser.add_argument("--module", type=str, default=None, help="Filter by module (Floor, Settle, Inventory, Settings, Reports, etc.)")
    parser.add_argument("--top-k", type=int, default=3, help="Number of results to return (default: 3)")
    parser.add_argument("--troubleshoot", action="store_true", help="Match query against troubleshooting matrix directly")
    parser.add_argument("--ai-context", action="store_true", help="Output token-budgeted AI context markdown for LLM prompt injection")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format for machine integration")
    parser.add_argument("--reindex", action="store_true", help="Rebuild the AI knowledge index")
    parser.add_argument("--benchmark", action="store_true", help="Run high-throughput latency benchmark")

    args = parser.parse_args()

    if args.reindex:
        build_ai_index()
        return

    engine = POSSearchEngine.get_instance()

    if args.benchmark:
        run_benchmark(engine)
        return

    if not args.query:
        parser.print_help()
        sys.exit(0)

    if args.ai_context:
        context_md = engine.get_ai_context(args.query, role=args.role, max_chunks=args.top_k)
        print(context_md)
        return

    if args.troubleshoot:
        results = engine.troubleshoot(args.query, top_k=args.top_k)
        if args.json:
            print(orjson.dumps(results, option=orjson.OPT_INDENT_2).decode("utf-8"))
            return

        print(f"\n🔍 [TROUBLESHOOTING SEARCH] Query: '{args.query}' (Latency: {results[0]['latency_ms'] if results else 0}ms)")
        print("=" * 80)
        if not results:
            print("No matching troubleshooting scenario found.")
        for r in results:
            print(f"\n⚠️  PROBLEM: {r['problem']} (Match Score: {r['match_score']})")
            print(f"✅  SOLUTION: {r['solution']}")
            print(f"📍  WHERE: {r['module']} -> {r['where']}")
            print(f"👥  ROLES: {', '.join(r['target_roles'])}")
            print("-" * 80)
        return

    results = engine.search(args.query, role=args.role, module=args.module, top_k=args.top_k)

    if args.json:
        print(orjson.dumps(results, option=orjson.OPT_INDENT_2).decode("utf-8"))
        return

    lat = results[0]["latency_ms"] if results else 0
    print(f"\n🔍 [POS SEARCH] Query: '{args.query}' | Found: {len(results)} | Latency: {lat}ms")
    print("=" * 80)

    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r['part']} - {r['section']} (Score: {r['score']})")
        print(f"    Module: {r['module']} | Location: {r['where']}")
        print(f"    Roles: {', '.join(r['target_roles'])}")
        print(f"    Summary: {r['summary']}")
        if r['steps']:
            print("    Steps:")
            for s in r['steps'][:4]:
                print(f"      {s}")
            if len(r['steps']) > 4:
                print(f"      ... (+{len(r['steps'])-4} more steps)")
        if r['key_notes']:
            print("    Key Notes:")
            for kn in r['key_notes'][:2]:
                print(f"      * {kn}")
        print("-" * 80)

if __name__ == "__main__":
    main()
