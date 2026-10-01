#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("public/leistungen/mehrfamilienhaeuser-kaufen-bochum.html").read_text(encoding="utf-8")
print("dropdown-item count", t.count("dropdown-item"))
print("--- dropdown snippets ---")
for m in re.finditer(r'.{0,20}dropdown-item.{0,100}', t):
    print(m.group(0).replace("\n", " ")[:180])
print("--- leistungen hrefs ---")
seen = []
for m in re.finditer(r'href="(/leistungen/[^"]+)"', t):
    if m.group(1) not in seen:
        seen.append(m.group(1))
print("\n".join(seen[:30]))
