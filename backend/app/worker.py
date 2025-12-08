import os
import shutil
import subprocess
from .jobs import get_job
from .models import get_conn
from datetime import datetime
import uuid
import tempfile

# Use temp directory that works on all platforms
WORKDIR = os.path.join(tempfile.gettempdir(), "testsight_workspace")
os.makedirs(WORKDIR, exist_ok=True)

def call_kiro_generate_tests(repo_path: str, spec_path: str = "/.kiro/generate_tests.spec.yaml") -> str:
    candidate = os.path.join(repo_path, ".kiro", "generated_tests.py")
    if os.path.exists(candidate):
        os.makedirs(os.path.join(repo_path, "tests"), exist_ok=True)
        dest = os.path.join(repo_path, "tests", "test_generated.py")
        shutil.copy(candidate, dest)
        return dest
    tests_dir = os.path.join(repo_path, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    dest = os.path.join(tests_dir, "test_generated.py")
    with open(dest, "w") as f:
        f.write("""
import pytest
from module_a import add

def test_add_positive():
    assert add(2,3) == 5

def test_add_zero():
    assert add(0,0) == 0
""")
    return dest

def run_pytest_with_coverage(repo_path: str):
    cmd = ["pytest", "--maxfail=1", "--disable-warnings", "--cov=.", "--cov-report=term-missing"]
    p = subprocess.Popen(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output, _ = p.communicate()
    tests_total = 0
    tests_failed = 0
    coverage = 0.0
    for line in output.splitlines():
        if "failed" in line and "passed" in line:
            parts = line.split(',')
            for part in parts:
                if 'passed' in part:
                    try:
                        passed = int(part.strip().split()[0])
                    except:
                        passed = 0
                if 'failed' in part:
                    try:
                        failed = int(part.strip().split()[0])
                    except:
                        failed = 0
            tests_failed = locals().get('failed', 0)
            tests_total = locals().get('passed', 0) + tests_failed
        if 'TOTAL' in line and '%' in line:
            try:
                coverage = float(line.split()[-1].strip().replace('%',''))
            except:
                pass
    return {"output": output, "tests_total": tests_total, "tests_failed": tests_failed, "coverage": coverage}

def save_run(job_id: int, res: dict, artifacts_path: str | None = None):
    conn = get_conn()
    cur = conn.cursor()
    started_at = datetime.utcnow().isoformat()
    finished_at = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO runs (job_id, started_at, finished_at, tests_total, tests_failed, coverage, artifacts_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (job_id, started_at, finished_at, res.get('tests_total',0), res.get('tests_failed',0), res.get('coverage',0.0), artifacts_path))
    conn.commit()
    conn.close()

def run_job_background(job_id: int):
    job = get_job(job_id)
    repo_url = job.get('repo_url')
    if repo_url.startswith("/") and os.path.exists(repo_url):
        repo_path = repo_url
    else:
        repo_name = f"repo_{uuid.uuid4().hex[:8]}"
        repo_path = os.path.join(WORKDIR, repo_name)
        os.makedirs(WORKDIR, exist_ok=True)
        try:
            subprocess.check_call(["git", "clone", repo_url, repo_path])
        except Exception as e:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE jobs SET status=? WHERE id=?", ("failed_clone", job_id))
            conn.commit()
            conn.close()
            return
    test_file = call_kiro_generate_tests(repo_path)
    res = run_pytest_with_coverage(repo_path)
    save_run(job_id, res)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET status=? WHERE id=?", ("done", job_id))
    conn.commit()
    conn.close()
