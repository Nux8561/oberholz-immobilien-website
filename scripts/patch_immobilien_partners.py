#!/usr/bin/env python3
"""Patch remaining coop/partners in immobilien + selected folders only (fast)."""

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bochum_audit_pass2 import process  # type: ignore

ROOT = Path(__file__).resolve().parents[1]

folders = [
    ROOT / "public" / "immobilien",
    ROOT / "public" / "ratgeber",
    ROOT / "public" / "whitepaper-generationenwechsel.html",
]

files: list[Path] = []
for item in [
    ROOT / "public" / "immobilien",
    ROOT / "public" / "ratgeber",
]:
    files.extend(item.rglob("*.html"))

# top-level whitepapers etc. that may still have old footer
for p in (ROOT / "public").glob("whitepaper-*.html"):
    files.append(p)
for p in (ROOT / "public").glob("*.html"):
    files.append(p)

files = sorted(set(files))
changed = 0
for i, path in enumerate(files, 1):
    original = path.read_text(encoding="utf-8", errors="replace")
    if not any(
        x in original
        for x in (
            "wuestenrot_bank_201x_logo.svg",
            "contentimg/32697_3_3.png",
            "kleinanzeigen.svg",
            "flowfact.png",
            "immowelt.png",
            "Münster, Essen, Bochum",
            "Münster, Essen und Bochum",
            "deutschlandweit",
            "ganz Deutschland",
        )
    ):
        continue
    html = process(original, strong=True, trust_links=("bekannt aus" in original.lower()))
    if html != original:
        path.write_text(html, encoding="utf-8")
        changed += 1
        print("updated", path.relative_to(ROOT))
print(f"Done. Changed {changed} / scanned {len(files)}")
