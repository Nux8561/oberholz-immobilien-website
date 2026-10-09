#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

pages = [
    Path("index.html"),
    Path("public/regionen/essen/immobilienmakler.html"),
    Path("public/regionen/essen/immobilie-verkaufen.html"),
    Path("public/regionen/bochum/immobilienmakler.html"),
    Path("public/regionen/muenster/immobilienmakler.html"),
]

for p in pages:
    t = p.read_text(encoding="utf-8", errors="ignore")
    idx = t.find('class="regio-goodie')
    print("==", p, "idx", idx)
    if idx < 0:
        continue
    start = t.rfind("<section", 0, idx)
    end = t.find("</section>", idx)
    chunk = t[start : end + 10]
    print("links:", re.findall(r'href="([^"]+)"', chunk))
    # title/h2
    h2 = re.search(r"<h2[^>]*>([\s\S]*?)</h2>", chunk)
    print("h2:", re.sub(r"\s+", " ", h2.group(1))[:120] if h2 else None)
    # nearby CTA after goodie
    after = t[end : end + 800]
    print("after links:", re.findall(r'href="([^"]+)"', after)[:8])
