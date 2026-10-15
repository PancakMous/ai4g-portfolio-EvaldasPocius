"""
Unified runner for NS Live Pulse.

Usage:
  python run.py               # Starts Live Dashboard + Autonomous Hourly Ingest (http://127.0.0.1:8000)
  python run.py --dashboard   # Starts Live Dashboard + Autonomous Hourly Ingest
  python run.py --fetch       # Fetches new live items once and scores them
  python run.py --evaluate    # Runs the 52-sample test benchmark
  python run.py --daemon      # Runs headless background loop (without web server)
  python run.py --interval 60 # Set polling interval in seconds (default 3600 = 1 hour)
"""

import os
import sys
import argparse

# Configure UTF-8 safe logging on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import uvicorn
from src.scheduler import run_pipeline_step, continuous_loop
from src.evaluate import run_evaluation
from src.storage import init_db, sync_static_bundle

def main():
    parser = argparse.ArgumentParser(description="NS Rail Live Pulse - Autonomous Stream Intelligence Runner")
    parser.add_argument("--dashboard", action="store_true", help="Launch interactive web dashboard with hourly background ingestion")
    parser.add_argument("--fetch", action="store_true", help="Fetch fresh live items once, score them, and update exports")
    parser.add_argument("--evaluate", action="store_true", help="Run the test benchmark against the 52 gold test items")
    parser.add_argument("--daemon", action="store_true", help="Run headless continuous ingestion loop without launching the dashboard")
    parser.add_argument("--interval", type=int, default=3600, help="Loop interval in seconds (default 3600 = 1 hour)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server to (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to (default 8000)")
    
    args = parser.parse_args()
    init_db()

    # Pass interval to background scheduler via environment variable
    os.environ["PULSE_POLL_INTERVAL"] = str(args.interval)

    # 1. Single Fetch Mode
    if args.fetch:
        print("[*] Fetching fresh live transit posts and analyzing sentiment...")
        new_count = run_pipeline_step(run_secondary=False, verbose=True)
        sync_static_bundle()
        print(f"[+] Done! Added {new_count} new posts and synced data/collected_posts.json + docs/index.html")
        return

    # 2. Evaluation Benchmark Mode
    if args.evaluate:
        print("[*] Running model benchmark evaluation (52 gold items)...")
        run_evaluation()
        return

    # 3. Headless Daemon Mode (no web server)
    if args.daemon:
        print(f"[*] Starting headless autonomous ingestion every {args.interval}s (1 hour)...")
        continuous_loop(interval_seconds=args.interval)
        return

    # 4. Default Mode: Interactive Dashboard with integrated Autonomous Hourly Scheduler
    print("=" * 75)
    print(" 🚆 NS Rail Live Pulse: Passenger Sentiment Radar")
    print(f" [*] Autonomous Hourly Ingest: ACTIVE (Polling every {args.interval}s / 1 hour)")
    print(f" [*] Live Web Dashboard URL:    http://{args.host}:{args.port}")
    print("=" * 75)
    
    uvicorn.run("src.app:app", host=args.host, port=args.port, reload=False)

if __name__ == "__main__":
    main()
