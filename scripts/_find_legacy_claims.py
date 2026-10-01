#!/usr/bin/env python3
from pathlib import Path
import re

files = [Path("index.html")]
for folder in ["public", "public/leistungen", "public/ueber-uns", "public/service", "public/ratgeber", "public/kontakt"]:
    files.extend(Path(folder).glob("*.html"))
    if folder.endswith("kontakt"):
        files.extend(Path(folder).glob("*/*.html"))

patterns = [
    r"11\.?000",
    r"1\.?200",
    r"zufriedene Kunden",
    r"Stammkunden",
    r"Serienkunden",
    r"bundesweiten? Netzwerk",
    r"hauseigenen Werbeagentur",
    r"Partnernetzwerk",
    r"ee-experten\.de",
    r"über \d+",
    r"mehr als \d+",
]

for pat in patterns:
    print("====", pat)
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r".{0,55}" + pat + r".{0,80}", t, re.I):
            s = m.group(0).replace("\n", " ")
            # skip css media queries
            if "min-width" in s or "zindex" in s or "setInterval" in s:
                continue
            print(p.as_posix(), "->", s[:160])
