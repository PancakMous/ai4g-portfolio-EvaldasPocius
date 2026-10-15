"""
FastAPI web server exposing REST endpoints for the dashboard and serving
the interactive frontend, featuring an autonomous hourly live ingestion scheduler.
"""

import os
import sys
import threading
import time
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager
from typing import Optional

# Ensure safe unicode handling on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.storage import (
    init_db,
    get_posts,
    get_sentiment_timeline,
    get_stats,
    sync_static_bundle
)
from src.scheduler import run_pipeline_step

HOURLY_INTERVAL = int(os.environ.get("PULSE_POLL_INTERVAL", 3600))  # Default 3600s = 1 hour
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

_scheduler_thread = None
_stop_event = threading.Event()
_scheduler_lock = threading.Lock()
_scheduler_state = {
    "is_live": True,
    "interval_seconds": HOURLY_INTERVAL,
    "status": "idle",
    "last_run": None,
    "next_run": None,
    "new_posts_last_run": 0,
    "last_error": None
}

def _hourly_background_worker():
    """Background worker thread running live ingestion every HOURLY_INTERVAL seconds."""
    print(f"[*] Autonomous Live Ingestion scheduler started (polling every {HOURLY_INTERVAL}s / 1 hour)")
    
    # Run first ingestion cycle on server startup
    try:
        with _scheduler_lock:
            _scheduler_state["status"] = "running"
            _scheduler_state["last_run"] = datetime.now(timezone.utc).isoformat()
        
        new_count = run_pipeline_step(run_secondary=False, verbose=True)
        
        with _scheduler_lock:
            _scheduler_state["new_posts_last_run"] = new_count
            _scheduler_state["status"] = "idle"
            _scheduler_state["last_error"] = None
    except Exception as e:
        print(f"[!] Error in initial startup ingestion: {e}")
        with _scheduler_lock:
            _scheduler_state["status"] = "idle"
            _scheduler_state["last_error"] = str(e)

    # Main hourly loop
    while not _stop_event.is_set():
        next_dt = datetime.now(timezone.utc) + timedelta(seconds=HOURLY_INTERVAL)
        with _scheduler_lock:
            _scheduler_state["next_run"] = next_dt.isoformat()
            
        # Sleep for HOURLY_INTERVAL seconds or exit early if stopped
        if _stop_event.wait(timeout=HOURLY_INTERVAL):
            break

        try:
            with _scheduler_lock:
                _scheduler_state["status"] = "running"
                _scheduler_state["last_run"] = datetime.now(timezone.utc).isoformat()
            
            print(f"\n[*] [HOURLY TRIGGER] Starting scheduled live ingest cycle at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}...")
            new_count = run_pipeline_step(run_secondary=False, verbose=True)
            
            with _scheduler_lock:
                _scheduler_state["new_posts_last_run"] = new_count
                _scheduler_state["status"] = "idle"
                _scheduler_state["last_error"] = None
        except Exception as e:
            print(f"[!] Error in scheduled hourly ingest: {e}")
            with _scheduler_lock:
                _scheduler_state["status"] = "idle"
                _scheduler_state["last_error"] = str(e)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler_thread, _stop_event
    init_db()
    sync_static_bundle()
    
    # Start autonomous background scheduler
    _stop_event.clear()
    _scheduler_thread = threading.Thread(target=_hourly_background_worker, daemon=True, name="LivePulseHourlyWorker")
    _scheduler_thread.start()
    
    yield
    
    # Graceful shutdown
    _stop_event.set()
    if _scheduler_thread and _scheduler_thread.is_alive():
        _scheduler_thread.join(timeout=2.0)
    print("[*] Autonomous Live Ingestion scheduler stopped.")

app = FastAPI(title="NS Live Pulse API", lifespan=lifespan)

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/stats")
async def api_stats():
    return get_stats()

@app.get("/api/timeline")
async def api_timeline(
    interval: str = Query("hour", pattern="^(hour|day)$"),
    hours: Optional[int] = Query(None, description="Limit timeline to recent hours (e.g. 24 or 168)")
):
    return get_sentiment_timeline(interval=interval, hours=hours)

@app.get("/api/posts")
async def api_posts(limit: int = 150, offset: int = 0, sentiment: str = None):
    return get_posts(limit=limit, offset=offset, sentiment_filter=sentiment)

@app.get("/api/status")
async def api_status():
    """Returns autonomous scheduler health, next scheduled hourly run, and last cycle metrics."""
    stats = get_stats()
    with _scheduler_lock:
        state = dict(_scheduler_state)
    state["total_posts"] = stats["total_posts"]
    state["latest_post_created"] = stats.get("latest_post")
    return state

@app.post("/api/refresh")
@app.get("/api/refresh")
async def api_refresh():
    """On-demand trigger for immediate live stream fetch and analysis."""
    try:
        new_saved = run_pipeline_step(run_secondary=False, verbose=True)
        stats = get_stats()
        with _scheduler_lock:
            _scheduler_state["last_run"] = datetime.now(timezone.utc).isoformat()
            _scheduler_state["new_posts_last_run"] = new_saved
            _scheduler_state["next_run"] = (datetime.now(timezone.utc) + timedelta(seconds=HOURLY_INTERVAL)).isoformat()
        return {
            "status": "success",
            "new_posts": new_saved,
            "total_posts": stats["total_posts"],
            "net_sentiment": stats["net_sentiment"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=False)
