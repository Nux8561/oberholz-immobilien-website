# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/service/finanzierungsrechner.html").read_text(encoding="utf-8", errors="ignore")

# Find object containing Baden-Württemberg rates
m = re.search(r'\{[^{}]*"Baden-Württemberg"\s*:\s*[\d.]+[^{}]*\}', t)
print("obj1", bool(m))
if m:
    print(m.group(0))

m2 = re.search(r"STATES\s*=\s*(\{.*?\})", t, re.S)
print("STATES", bool(m2))
if m2:
    print(m2.group(1)[:1200])

# broader: from Baden-Württemberg rate to closing brace
idx = t.find('"Baden-Württemberg":')
print("idx", idx)
if idx >= 0:
    chunk = t[idx - 40 : idx + 600]
    print(chunk)
