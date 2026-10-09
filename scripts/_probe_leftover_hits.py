#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

paths = [
    Path("index.html"),
    Path("public/leistungen.html"),
]

needles = [
    "zertifizierten Immobiliengutachter",
    "Immobilienmakler Bochum",
    "in Bochum und Umgebung",
    "Energieberatung",
    "Gutachterkompetenz",
    "Energiekompetenz",
]

for path in paths:
    t = path.read_text(encoding="utf-8", errors="ignore")
    print("====", path)
    for n in needles:
        for m in re.finditer(re.escape(n), t):
            start = max(0, m.start() - 60)
            end = min(len(t), m.end() + 80)
            print(n, "=>", repr(t[start:end]))
            print("---")
