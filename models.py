import sqlite3
from pydantic import BaseModel
from datetime import datetime
import os

# Use a relative path that works on all platforms
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB = os.environ.get("TESTSIGHT_DB", os.path.join(DB_DIR, "test_sight.db"))

# DB helper
def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_url TEXT,
        created_at TEXT,
        status TEXT,
        commit_sha TEXT,
        language TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        started_at TEXT,
        finished_at TEXT,
        tests_total INTEGER,
        tests_failed INTEGER,
        coverage REAL,
        artifacts_path TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_type TEXT,
        language TEXT,
        input_data TEXT,
        output_data TEXT,
        status TEXT,
        created_at TEXT,
        user_id TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Activity log helper
def log_activity(activity_type: str, language: str, input_data: str, output_data: str, status: str = "success"):
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO activity_logs (activity_type, language, input_data, output_data, status, created_at, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (activity_type, language, input_data[:500], output_data[:1000], status, created_at, "default_user"))
    conn.commit()
    log_id = cur.lastrowid
    conn.close()
    return log_id

def get_activity_logs(limit: int = 50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM activity_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class Job(BaseModel):
    id: int
    repo_url: str
    created_at: str
    status: str
    commit_sha: str | None = None

class Run(BaseModel):
    id: int
    job_id: int
    started_at: str
    finished_at: str | None = None
    tests_total: int | None = 0
    tests_failed: int | None = 0
    coverage: float | None = 0.0
    artifacts_path: str | None = None
