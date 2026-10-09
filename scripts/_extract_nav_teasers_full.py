#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")

print("teaser count", t.count("nav-overview-teaser"))
print("overview-img count", t.count("nav-overview-img"))
print("muenchen count", t.count("muenchen.jpg"))

# Extract every overview col block briefly
for m in re.finditer(
    r'<div class="col-12 col-xl-3 nav-overview-col">([\s\S]*?)</div>\s*<div class="col-12 col-xl-9">',
    t,
):
    block = m.group(1)
    title = re.search(r"<strong>([^<]+)</strong>", block)
    imgs = re.findall(r'src="([^"]+)"', block)
    teasers = len(re.findall(r"nav-overview-teaser", block))
    print("OVERVIEW", title.group(1) if title else "?", "imgs", imgs, "teasers", teasers)
