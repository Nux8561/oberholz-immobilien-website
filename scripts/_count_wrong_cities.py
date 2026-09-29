# -*- coding: utf-8 -*-
"""Count how many HTML files contain wrong city makler links (fast byte scan)."""
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NEEDLES = [
    b"immobilienmakler-hamburg.html",
    b"immobilienmakler-stuttgart.html",
    b"immobilienmakler-muenchen.html",
    b"immobilienmakler-duesseldorf.html",
    b"immobilienmakler-hannover.html",
    b"immobilienmakler-frankfurt-am-main.html",
    b"immobilienmakler-villingen-schwenningen.html",
    b"Immobilienmakler Stuttgart",
    b"Immobilienmakler Hamburg",
    b"Immobilienmakler M\xc3\xbcnchen",
]

roots = [Path("index.html")] + list(Path("public").rglob("*.html"))
# also check if root has more html
roots += [p for p in Path(".").glob("*.html") if p.name != "index.html"]

hits = 0
sample = []
for p in roots:
    try:
        raw = p.read_bytes()
    except OSError:
        continue
    if any(n in raw for n in NEEDLES):
        hits += 1
        if len(sample) < 15:
            sample.append(str(p.as_posix()))

print("files_with_wrong_cities", hits)
print("total_html_checked", len(roots))
print("sample:")
for s in sample:
    print(" ", s)
