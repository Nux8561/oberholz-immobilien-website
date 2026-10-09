#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")
srcs = re.findall(
    r'nav-overview-teaser__img[^>]*src="([^"]+)"|src="([^"]+)"[^>]*nav-overview-teaser__img',
    t,
)
flat = [a or b for a, b in srcs]
print("teaser imgs", sorted(set(flat)))
# any img near empty col after leistungen items
i = t.find('href="/leistungen/immobilienvermarktung.html"')
print(repr(t[i : i + 400]))
