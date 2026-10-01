#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("public/theme/contact-widget.html").read_text(encoding="utf-8")
# strip style
body = re.sub(r"<style[\s\S]*?</style>", "", t, count=1)
# find name-ish text near facepile / header
for pat in ["Streit", "Oberholz", "Michael", "Kersten", "Leiter", "header-meta", "facepile"]:
    print(pat, body.find(pat))

m = re.search(r'class="cw-header"[\s\S]{0,2500}', body)
Path("scripts/_cw_header_now.txt").write_text(m.group(0) if m else "none", encoding="utf-8")
print("wrote header snip", len(m.group(0) if m else ""))
