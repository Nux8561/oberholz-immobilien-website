#!/usr/bin/env python3
from pathlib import Path
import re
import urllib.request

t = Path("public/media/_interhyp.html").read_text(encoding="utf-8", errors="replace")
# find svg/png logo candidates
cands = []
for m in re.finditer(r"(https?://[^\"'\s>]+\.(?:svg|png|jpg|webp))", t, re.I):
    u = m.group(1)
    if any(k in u.lower() for k in ("logo", "brand", "header", "interhyp")):
        cands.append(u)
for m in re.finditer(r'["\'](/[^"\']+\.(?:svg|png))["\']', t, re.I):
    u = m.group(1)
    if any(k in u.lower() for k in ("logo", "brand", "header")):
        cands.append("https://www.interhyp.de" + u)

print("candidates", len(set(cands)))
for u in sorted(set(cands))[:40]:
    print(u)

# also search for swisslife from a better page
for src in ["_swiss.html", "_dvag.html"]:
    t2 = Path("public/media") / src
    raw = t2.read_text(encoding="utf-8", errors="replace")
    print("====", src)
    for m in re.finditer(r"(https?://[^\"'\s>]+\.(?:svg|png))", raw, re.I):
        if "logo" in m.group(1).lower():
            print(m.group(1))
    for m in re.finditer(r'["\'](/[^"\']*logo[^"\']*\.(?:svg|png))["\']', raw, re.I):
        print(m.group(1))
