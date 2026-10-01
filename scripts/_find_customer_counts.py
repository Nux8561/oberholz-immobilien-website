#!/usr/bin/env python3
from pathlib import Path
import re

files = list(Path("public").rglob("*.html")) + [Path("index.html")]
skip = {"regionen", "immopedia", "dist", "node_modules"}
hits = {}
for p in files:
    if any(s in p.parts for s in skip):
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(
        r".{0,35}(\+?\d{1,3}\.?\d{3})\s*zufriedene Kunden.{0,25}"
        r"|.{0,40}(11\.000|14\.700|1\.200)\s*(Stamm|Serien|Kunden)?.{0,50}",
        t,
        re.I,
    ):
        s = m.group(0).replace("\n", " ")
        if any(x in s for x in ("min-width", "breakpoint", 'height="1200"', "data-val", "setTimeout")):
            continue
        hits.setdefault(s[:160], []).append(str(p))

for s, ps in hits.items():
    print(s)
    print(" ", len(ps), "e.g.", ps[0])
