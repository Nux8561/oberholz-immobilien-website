# -*- coding: utf-8 -*-
"""Patch ALL HTML under public/ (esp. regionen) for Oberholz standorte. Streaming + progress."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fix_standorte_fast import patch_html_text  # noqa: E402

NEEDLES = [
    b"immobilienmakler-hamburg.html",
    b"immobilienmakler-stuttgart.html",
    b"immobilienmakler-muenchen.html",
    b"immobilienmakler-duesseldorf.html",
    b"immobilienmakler-hannover.html",
    b"immobilienmakler-frankfurt",
    b"immobilienmakler-villingen",
    b"Immobilienmakler Stuttgart",
    b"Immobilienmakler Hamburg",
    b"bundesweit und auch regional",
]

SKIP_DIRS = {"media", "mediatypes", "theme", "assets", ".git", "node_modules"}


def main() -> None:
    start = time.time()
    checked = 0
    scanned = 0
    changed = 0
    errors = 0
    totals = {"desktop": 0, "mobile": 0, "tbody": 0, "href": 0, "label": 0, "text": 0}

    for root, dirs, files in os.walk(ROOT / "public"):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not name.endswith(".html"):
                continue
            checked += 1
            path = Path(root) / name
            try:
                raw = path.read_bytes()
            except OSError:
                errors += 1
                continue
            if not any(n in raw for n in NEEDLES):
                if checked % 2000 == 0:
                    print(f"... checked {checked} scanned {scanned} changed {changed} ({time.time()-start:.0f}s)", flush=True)
                continue
            scanned += 1
            text = raw.decode("utf-8", errors="ignore")
            new_text, stats = patch_html_text(text)
            if new_text != text:
                try:
                    path.write_text(new_text, encoding="utf-8")
                    changed += 1
                    for k, v in stats.items():
                        totals[k] += v
                except OSError:
                    errors += 1
            if scanned % 200 == 0 or changed % 200 == 0:
                print(f"... checked {checked} scanned {scanned} changed {changed} ({time.time()-start:.0f}s)", flush=True)

    # also index.html at root
    idx = ROOT / "index.html"
    if idx.exists():
        raw = idx.read_bytes()
        if any(n in raw for n in NEEDLES):
            text = raw.decode("utf-8", errors="ignore")
            new_text, stats = patch_html_text(text)
            if new_text != text:
                idx.write_text(new_text, encoding="utf-8")
                changed += 1
                print("patched index.html", stats)

    print("DONE checked", checked, "scanned", scanned, "changed", changed, "errors", errors)
    print("totals", totals)
    print(f"elapsed {time.time()-start:.1f}s")


if __name__ == "__main__":
    main()
