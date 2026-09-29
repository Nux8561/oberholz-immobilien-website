# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = Path("public/regionen.html")
if not p.exists():
    # try root
    for cand in Path("public").rglob("*regionen*"):
        print("found", cand)
    sys.exit(0)

t = p.read_text(encoding="utf-8", errors="ignore")
print("len", len(t))
print("title", re.search(r"<title>(.*?)</title>", t).group(1))
for city in ["Stuttgart", "München", "Hamburg", "Münster", "Essen", "Bochum", "Frankfurt", "Hannover"]:
    print(city, t.count(city))
# list makler links
for m in re.finditer(r'href="([^"]*immobilienmakler[^"]*)"', t):
    print("link", m.group(1))
