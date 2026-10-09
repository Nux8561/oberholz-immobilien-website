#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = [root / "index.html"] + list((root / "public").rglob("*.html"))
pat = re.compile(
    r".{0,50}(?:9(?:&nbsp;|\s)?Bewertungen|reviewCount[^0-9]{0,20}9(?!\d)|\"reviewCount\"\s*:\s*9(?!\d)).{0,50}",
    re.I,
)
hits = []
for f in files:
    t = f.read_text(encoding="utf-8", errors="ignore")
    if "9 Bewertungen" not in t and "9&nbsp;Bewertungen" not in t and "reviewCount" not in t:
        continue
    for m in pat.finditer(t):
        snippet = m.group(0).replace("\n", " ")
        if "28" in snippet and "9 Bewertungen" not in snippet and "9&nbsp;Bewertungen" not in snippet:
            continue
        # skip false positives like 19 Bewertungen if any
        if re.search(r"(?<![0-9])9(?:&nbsp;|\s)?Bewertungen", snippet) or re.search(
            r"reviewCount[^0-9]{0,20}(?<![0-9])9(?![0-9])", snippet
        ) or re.search(r'"reviewCount"\s*:\s*9(?![0-9])', snippet):
            hits.append((str(f.relative_to(root)), snippet[:140]))

print(f"hits={len(hits)}")
for path, snip in hits[:40]:
    print("---", path)
    print(snip)
