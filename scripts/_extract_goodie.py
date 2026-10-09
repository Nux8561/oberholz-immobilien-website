#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")

# Find content block with class regio-goodie (not CSS)
pat = re.compile(
    r'(<section[^>]*>\s*<div class="container">\s*'
    r'<div class="regio-goodie[\s\S]*?</div>\s*</div>\s*</section>)',
    re.I,
)
m = pat.search(t)
if not m:
    # broader: from section that contains the content div
    idx = t.find('<div class="regio-goodie p-4')
    if idx < 0:
        idx = t.find('class="regio-goodie p-4')
    print("idx", idx)
    if idx >= 0:
        start = t.rfind("<section", 0, idx)
        end = t.find("</section>", idx)
        print("start", start, "end", end)
        chunk = t[start : end + len("</section>")]
        print(chunk[:3000])
        print("---LINKS---")
        for href in re.findall(r'href="([^"]+)"', chunk):
            print(href)
else:
    chunk = m.group(1)
    print("FOUND", len(chunk))
    print(chunk[:3000])
    print("---LINKS---")
    for href in re.findall(r'href="([^"]+)"', chunk):
        print(href)

# also count occurrences across site
count = 0
for p in [Path("index.html"), *Path("public").rglob("*.html")]:
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        continue
    if 'class="regio-goodie' in txt or "regio-goodie p-4" in txt:
        if "background: linear-gradient" in txt and txt.count("regio-goodie") <= 5:
            # might be only CSS
            if 'class="regio-goodie' not in txt and "regio-goodie p-4" not in txt:
                continue
        if 'class="regio-goodie' in txt:
            count += 1
            if count <= 15:
                print("PAGE", p)
print("total pages with class=", count)
