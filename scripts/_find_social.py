#!/usr/bin/env python3
from pathlib import Path
import re

files = [Path("index.html")] + list(Path("public").glob("*.html"))
files += list(Path("public/leistungen").glob("*.html"))
files += list(Path("public/kontakt").glob("*.html"))

for path in files:
    t = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for m in re.finditer(r'.{0,60}(youtube|youtu\.be|instagram|facebook\.com|linkedin|xing)[^"\'<\s]*.{0,40}', t, re.I):
        hits.append(m.group(0).replace("\n", " ")[:140])
    if hits:
        print("==", path)
        for h in hits[:8]:
            print(" ", h)
