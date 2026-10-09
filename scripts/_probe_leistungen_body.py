#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("public/leistungen.html").read_text(encoding="utf-8")
print("len", len(t))
hrefs = re.findall(r'href="(/leistungen/[^"]+)"', t)
print("hrefs", hrefs)
print("card", t.count("card-"))
m = re.search(r"<h1[\s\S]{0,3000}", t)
print(m.group(0)[:1800] if m else None)
