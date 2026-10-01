#!/usr/bin/env python3
from pathlib import Path

needles = ["pages.dev", "Lokale Ansicht", "profilbild_mayer", "cw-local-overlay"]
files = [Path("index.html")]
files += list(Path("public").glob("*.html"))
files += list(Path("public/leistungen").glob("*.html"))
files += list(Path("public/kontakt").glob("*.html"))

for needle in needles:
    hits = []
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace")
        if needle in t:
            hits.append(str(p))
    print(needle, len(hits))
    for h in hits[:8]:
        print(" ", h)
