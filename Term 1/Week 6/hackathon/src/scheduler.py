"""
Continuous pipeline runner for NS Live Pulse.
Periodically fetches new items from Reddit & Fediverse/Mastodon,
runs RobBERT sentiment analysis, and persists into SQLite and static bundles.
"""

import sys
import time
import argparse
from datetime import datetime, timezone

# Ensure Unicode (emojis) prints properly on Windows consoles without charmap crash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.fetcher import fetch_all_transit_posts
from src.models import analyze_sentiment
from src.storage import init_db, save_post, get_stats, post_exists, sync_static_bundle

def safe_str(text: str, max_len: int = 65) -> str:
    """Sanitizes text for safe console logging on any terminal."""
    if not text:
        return ""
    clean = text.replace("\n", " ").strip()[:max_len]
    return clean.encode("ascii", errors="replace").decode("ascii")

def run_pipeline_step(run_secondary: bool = False, verbose: bool = True) -> int:
    """
    Executes a single fetch -> analyse -> store cycle.
    Only runs transformer analysis on truly new posts to maintain peak performance.
    Returns number of new items saved.
    """
    start_time = datetime.now(timezone.utc)
    if verbose:
        print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}] Fetching fresh transit items...")
    
    posts = fetch_all_transit_posts()
    new_candidates = [p for p in posts if not post_exists(p["id"])]
    
    if verbose:
        print(f" -> Fetched {len(posts)} stream items ({len(new_candidates)} fresh, {len(posts) - len(new_candidates)} already stored)")
    
    new_saved = 0
    for p in new_candidates:
        # Check sentiment with pre-trained Dutch transformer for new items
        analysis = analyze_sentiment(p["text"], run_secondary=run_secondary)
        p["primary_sentiment"] = analysis["primary_sentiment"]
        p["primary_score"] = analysis["primary_score"]
        p["secondary_sentiment"] = analysis["secondary_sentiment"]
        p["secondary_score"] = analysis["secondary_score"]
        
        saved = save_post(p)
        if saved:
            new_saved += 1
            if verbose:
                print(f"  + New post [{p['id']}] [{p['primary_sentiment']}|{p['primary_score']}]: {safe_str(p['text'])}...")

    # Always keep static exports and dashboard data synced
    sync_static_bundle()

    if verbose:
        stats = get_stats()
        print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}] Cycle complete: +{new_saved} new posts added. Total stored: {stats['total_posts']} (Net Sentiment: {stats['net_sentiment']})")
    
    return new_saved

def continuous_loop(interval_seconds: int = 3600, run_secondary: bool = False) -> None:
    """Runs autonomous continuous background loop polling every interval_seconds (default: 3600s / 1 hour)."""
    init_db()
    print(f"=== Starting NS Live Pulse Autonomous Pipeline (Hourly Interval: {interval_seconds}s) ===")
    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n--- Ingestion Cycle #{cycle} ---")
            run_pipeline_step(run_secondary=run_secondary, verbose=True)
            next_time = datetime.now(timezone.utc).timestamp() + interval_seconds
            print(f"Sleeping for {interval_seconds}s until next hourly run at {datetime.fromtimestamp(next_time, timezone.utc).strftime('%H:%M:%S UTC')}...")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nPipeline gracefully stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NS Live Pulse autonomous continuous runner")
    parser.add_argument("--once", action="store_true", help="Run a single ingest cycle and exit")
    parser.add_argument("--interval", type=int, default=3600, help="Polling interval in seconds (default: 3600 = 1 hour)")
    parser.add_argument("--with-secondary", action="store_true", help="Also run secondary model")
    args = parser.parse_args()

    init_db()
    if args.once:
        run_pipeline_step(run_secondary=args.with_secondary, verbose=True)
    else:
        continuous_loop(interval_seconds=args.interval, run_secondary=args.with_secondary)
