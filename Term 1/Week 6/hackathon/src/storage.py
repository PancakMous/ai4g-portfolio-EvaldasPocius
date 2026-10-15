"""
Database module for storing and querying collected transit posts and sentiment scores.
Supports SQLite storage and JSON export.
"""

import sqlite3
import json
import os
import re
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pulse.db")

def init_db(db_path: str = DB_PATH) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL,
                fetched_at TEXT NOT NULL,
                text TEXT NOT NULL,
                url TEXT,
                primary_sentiment TEXT,
                primary_score REAL,
                secondary_sentiment TEXT,
                secondary_score REAL,
                language TEXT DEFAULT 'nl'
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_sentiment ON posts(primary_sentiment)")
        conn.commit()

def post_exists(post_id: str, db_path: str = DB_PATH) -> bool:
    """Checks whether a post ID is already persisted in the database."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM posts WHERE id = ? LIMIT 1", (post_id,))
            return cursor.fetchone() is not None
    except Exception:
        return False

def save_post(post: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    """Inserts a post if not already existing. Returns True if inserted, False if duplicate."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO posts (
                    id, source, created_at, fetched_at, text, url,
                    primary_sentiment, primary_score, secondary_sentiment, secondary_score, language
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                post["id"],
                post["source"],
                post["created_at"],
                post.get("fetched_at", datetime.now(timezone.utc).isoformat()),
                post["text"],
                post.get("url", ""),
                post.get("primary_sentiment"),
                post.get("primary_score"),
                post.get("secondary_sentiment"),
                post.get("secondary_score"),
                post.get("language", "nl")
            ))
            inserted = cursor.rowcount > 0
            conn.commit()
            return inserted
    except Exception as e:
        print(f"Error saving post {post.get('id')}: {e}")
        return False

def get_posts(limit: int = 200, offset: int = 0, sentiment_filter: Optional[str] = None, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM posts"
        params = []
        if sentiment_filter:
            query += " WHERE primary_sentiment = ?"
            params.append(sentiment_filter)
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

def get_sentiment_timeline(interval: str = "hour", hours: Optional[int] = None, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Aggregates sentiment by time bucket (hourly or daily), with optional recent hours filter."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # SQLite strftime format: %Y-%m-%d %H:00 or %Y-%m-%d
        date_fmt = "%Y-%m-%d %H:00" if interval == "hour" else "%Y-%m-%d"
        
        where_clause = "WHERE created_at IS NOT NULL"
        params = []
        if hours:
            where_clause += " AND created_at >= datetime('now', ?)"
            params.append(f"-{hours} hours")
        
        cursor.execute(f"""
            SELECT 
                strftime('{date_fmt}', created_at) as time_bucket,
                COUNT(*) as total_count,
                SUM(CASE WHEN primary_sentiment = 'positive' THEN 1 ELSE 0 END) as positive_count,
                SUM(CASE WHEN primary_sentiment = 'neutral' THEN 1 ELSE 0 END) as neutral_count,
                SUM(CASE WHEN primary_sentiment = 'negative' THEN 1 ELSE 0 END) as negative_count,
                AVG(primary_score) as avg_confidence
            FROM posts
            {where_clause}
            GROUP BY time_bucket
            ORDER BY time_bucket ASC
        """, params)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            d = dict(r)
            total = d["total_count"]
            # Pulse index: Net Sentiment score from -100 to +100
            # ((Pos - Neg) / Total) * 100
            net_sentiment = round(((d["positive_count"] - d["negative_count"]) / total) * 100, 1) if total > 0 else 0
            d["net_sentiment"] = net_sentiment
            results.append(d)
        return results

def get_stats(db_path: str = DB_PATH) -> Dict[str, Any]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM posts")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts WHERE primary_sentiment = 'positive'")
        pos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts WHERE primary_sentiment = 'neutral'")
        neu = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts WHERE primary_sentiment = 'negative'")
        neg = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM posts")
        earliest, latest = cursor.fetchone()
        
        return {
            "total_posts": total,
            "positive_count": pos,
            "neutral_count": neu,
            "negative_count": neg,
            "earliest_post": earliest,
            "latest_post": latest,
            "net_sentiment": round(((pos - neg) / total) * 100, 1) if total > 0 else 0
        }

def export_json(output_path: str, db_path: str = DB_PATH) -> int:
    posts = get_posts(limit=100000, db_path=db_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    return len(posts)

def sync_static_bundle(base_dir: str = None, db_path: str = DB_PATH) -> None:
    """Updates collected_posts.json, docs/pulse_data.json, and docs/index.html with fresh state."""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
    
    data_dir = os.path.join(base_dir, "data")
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    
    stats = get_stats(db_path=db_path)
    timeline = get_sentiment_timeline(interval="hour", db_path=db_path)
    posts = get_posts(limit=250, db_path=db_path)
    
    # 1. Update data/collected_posts.json
    export_json(os.path.join(data_dir, "collected_posts.json"), db_path=db_path)
    
    # 2. Update docs/pulse_data.json
    bundle = {
        "stats": stats,
        "timeline": timeline,
        "posts": posts,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    with open(os.path.join(docs_dir, "pulse_data.json"), "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
        
    # 3. Synchronize docs/index.html embedded cache if present
    docs_index = os.path.join(docs_dir, "index.html")
    if os.path.exists(docs_index):
        try:
            with open(docs_index, "r", encoding="utf-8") as f:
                content = f.read()
            
            content = re.sub(
                r'const EMBEDDED_STATS\s*=\s*\{.*?\};',
                lambda m: f'const EMBEDDED_STATS = {json.dumps(stats)};',
                content
            )
            content = re.sub(
                r'const EMBEDDED_TIMELINE\s*=\s*\[.*?\];',
                lambda m: f'const EMBEDDED_TIMELINE = {json.dumps(timeline)};',
                content
            )
            content = re.sub(
                r'const EMBEDDED_POSTS\s*=\s*\[.*?\];',
                lambda m: f'const EMBEDDED_POSTS = {json.dumps(posts)};',
                content
            )
            with open(docs_index, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Warning updating docs/index.html: {e}")
