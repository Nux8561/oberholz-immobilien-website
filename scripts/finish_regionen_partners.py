#!/usr/bin/env python3
"""Finish remaining Wüstenrot/coop leftovers under public/regionen (byte-marker scan)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bochum_audit_pass2 import process  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "public" / "regionen"

MARKERS = (
    b"wuestenrot_bank_201x_logo.svg",
    b"contentimg/32697_3_3.png",
    b"kleinanzeigen.svg",
    b"flowfact.png",
    b"immowelt.png",
)

changed = 0
scanned = 0
hits = 0
for path in REG.rglob("*.html"):
    scanned += 1
    data = path.read_bytes()
    if not any(m in data for m in MARKERS):
        if scanned % 2000 == 0:
            print(f"scanned {scanned}, hits {hits}, changed {changed}", flush=True)
        continue
    hits += 1
    original = data.decode("utf-8", errors="replace")
    html = process(original, strong=False, trust_links=False)
    # Bochum-city pages: stronger copy
    if "bochum" in path.as_posix().lower():
        html = process(original, strong=True, trust_links=("bekannt aus" in original.lower()))
        html = html.replace("Münster, Essen, Bochum", "Bochum, Münster")
        html = html.replace("Münster, Essen und Bochum", "Bochum und Münster")
    if html != original:
        path.write_text(html, encoding="utf-8")
        changed += 1
        print("updated", path.relative_to(ROOT), flush=True)
    if scanned % 2000 == 0:
        print(f"scanned {scanned}, hits {hits}, changed {changed}", flush=True)

print(f"Done. scanned={scanned} hits={hits} changed={changed}", flush=True)
