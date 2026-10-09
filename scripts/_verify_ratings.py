#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

pages = [
    Path("index.html"),
    Path("public/regionen.html"),
    Path("public/leistungen.html"),
    Path("public/immobilien.html"),
]
for p in pages:
    t = p.read_text(encoding="utf-8", errors="ignore")
    print("==", p)
    print("  4.9", t.count("4.9"), "5.0", t.count("5.0"))
    print("  9 Bewertungen", t.count("9 Bewertungen"), "28 Bewertungen", t.count("28 Bewertungen"))
    print("  reviewCount", re.findall(r'"reviewCount":\s*\d+', t)[:3])
    for m in re.finditer(r".{0,20}5\.0/5.{0,40}", t):
        s = m.group(0)
        if "Bewertung" in s or "Sehr" in s or "fw-bold" in s or "strong" in s:
            print("  ctx", repr(s[:80]))
            break
