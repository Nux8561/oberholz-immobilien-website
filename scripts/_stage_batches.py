#!/usr/bin/env python3
"""Stage all changed files in small batches to avoid OneDrive/git lock issues."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PREFIXES = ("dist-regionen/", "scripts/__pycache__/")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True)


def clear_lock() -> None:
    lock = ROOT / ".git" / "index.lock"
    if lock.exists():
        try:
            lock.unlink()
        except OSError:
            time.sleep(0.5)
            try:
                lock.unlink()
            except OSError:
                pass


def porcelain() -> list[str]:
    p = run(["git", "status", "--porcelain", "-u"])
    paths: list[str] = []
    for line in p.stdout.splitlines():
        if not line or len(line) < 4:
            continue
        path = line[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if any(path.startswith(s) or path.replace("\\", "/").startswith(s) for s in SKIP_PREFIXES):
            continue
        paths.append(path.replace("\\", "/"))
    return paths


def add_batch(paths: list[str]) -> bool:
    clear_lock()
    p = run(["git", "add", "--"] + paths)
    if p.returncode != 0:
        print("FAIL batch", paths[0], p.stderr[:300])
        clear_lock()
        return False
    return True


def main() -> None:
    paths = porcelain()
    print("to stage", len(paths), flush=True)
    ok = 0
    batch_size = 80
    for i in range(0, len(paths), batch_size):
        batch = paths[i : i + batch_size]
        if add_batch(batch):
            ok += len(batch)
        else:
            # retry one-by-one
            for path in batch:
                if add_batch([path]):
                    ok += 1
        if (i // batch_size) % 10 == 0:
            print(f"progress {min(i + batch_size, len(paths))}/{len(paths)} ok={ok}", flush=True)
    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    print("staged total", len(staged), flush=True)


if __name__ == "__main__":
    main()
