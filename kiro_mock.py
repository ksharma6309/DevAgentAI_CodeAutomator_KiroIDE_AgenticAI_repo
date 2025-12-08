# kiro_mock.py
# Usage (simulates): python kiro_mock.py run <spec_path> --repo <repo_path>
import sys
import shutil
import os

def usage():
    print("kiro_mock: Usage: run <spec> --repo <repo_path>")
    sys.exit(1)

def main(argv):
    if len(argv) < 2:
        usage()
    cmd = argv[1]
    if cmd != "run":
        usage()
    # parse args: look for --repo <path>
    repo = None
    for i,a in enumerate(argv):
        if a == "--repo" and i+1 < len(argv):
            repo = argv[i+1]
    if not repo:
        print("kiro_mock: missing --repo <repo_path>")
        sys.exit(1)
    # Look for a generated tests file in the project .kiro of the sample repo path or spec folder
    # We'll try these candidate sources (project-root .kiro, and repo/.kiro)
    cand_sources = [
        os.path.join(os.getcwd(), ".kiro", "generated_tests.py"),
        os.path.join(repo, ".kiro", "generated_tests.py"),
        os.path.join(os.getcwd(), "sample_repos", "sample_project_a", ".kiro", "generated_tests.py"),
        os.path.join(os.getcwd(), "sample_repos", "sample_project_b", ".kiro", "generated_tests.py"),
    ]
    src = None
    for c in cand_sources:
        if os.path.exists(c):
            src = c
            break
    if not src:
        print("kiro_mock: no generated_tests.py found in candidates; nothing to copy.")
        sys.exit(2)
    dst_dir = os.path.join(repo, "tests")
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, "test_generated.py")
    shutil.copy(src, dst)
    print(f"kiro_mock: copied {src} -> {dst}")
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
