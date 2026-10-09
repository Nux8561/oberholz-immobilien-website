#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")

for label in ["Leistungen", "Service", "Über uns", "Kontakt"]:
    i = t.find(f'title="{label}"')
    print("==", label, i)
    # find following dropdown-menu
    dm = t.find('class="dropdown-menu', i)
    if dm < 0:
        continue
    chunk = t[dm : dm + 3500]
    teasers = re.findall(r"nav-overview-teaser[\s\S]{0,500}", chunk)
    imgs = re.findall(r"<img[^>]+>", chunk)
    print(" teasers", len(teasers), "imgs", len(imgs))
    for img in imgs:
        print(" ", img[:250])
    if "leaf-watermark" in chunk or "background-image" in chunk[:200]:
        print(" has watermark css nearby")

# Find leaf watermark CSS full rule
m = re.search(r"#navbarmain \.dropdown-menu \{[^}]+leaf-watermark[^}]+\}", t)
if m:
    print("WATERMARK RULE", m.group(0)[:500])
else:
    # broader
    m = re.search(r"leaf-watermark[\s\S]{0,200}", t)
    print("WATERMARK CTX", m.group(0) if m else None)

# Check if file exists
wm = Path("public/theme/public/assets/frontend/images/leaf-watermark.svg")
print("wm exists", wm.exists())
if wm.exists():
    print(wm.read_text(encoding="utf-8", errors="ignore")[:300])
