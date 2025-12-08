from .models import get_conn
from datetime import datetime


def create_job(repo_url: str):
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    status = "queued"
    cur.execute("INSERT INTO jobs (repo_url, created_at, status) VALUES (?, ?, ?)", (repo_url, created_at, status))
    conn.commit()
    job_id = cur.lastrowid
    conn.close()
    return {"id": job_id, "repo_url": repo_url, "created_at": created_at, "status": status}

def get_job(job_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)

def list_jobs():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
