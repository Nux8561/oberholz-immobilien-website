#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")

# Hero / banner person images
for pat in [
    r"/media/bannerright[^\"'\s]+",
    r"/media/[^\"'\s]*penn[^\"'\s]*",
    r"/media/[^\"'\s]*oberholz[^\"'\s]*",
    r"/media/team[^\"'\s]+",
    r"/media/[^\"'\s]*t7a[^\"'\s]+",
]:
    found = sorted(set(re.findall(pat, t, re.I)))
    if found:
        print(pat, "=>")
        for f in found[:20]:
            print(" ", f)

# CSS referencing images in style near dropdown
for m in re.finditer(r"dropdown-menu[^{]{0,80}\{[^}]{0,400}\}", t):
    if "url(" in m.group(0) or "background" in m.group(0):
        print("CSS", m.group(0)[:300])

# Check analysis header for img in leistungen menu
h = Path("analysis/header.html").read_text(encoding="utf-8", errors="ignore")
i = h.find("Immobilienbewertung")
print("analysis around", repr(h[i : i + 800]) if i > 0 else None)
