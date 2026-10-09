#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("index.html").read_text(encoding="utf-8")

for m in re.finditer(r'nav-overview-img[^>]*>|<img[^>]*nav-overview-img[^>]*>', t):
    start = max(0, m.start() - 200)
    print(repr(t[start : m.end() + 50]))
    print("---")

print("all pillar-card:", sorted(set(re.findall(r"/media/pillar-card/[^\"']+", t))))
print("michael-oberholz exists", Path("public/media/oberholz-team/michael-oberholz.png").exists())
print("muenchen exists", Path("public/media/pillar-card/muenchen.jpg").exists())
