from pathlib import Path
import re
from collections import Counter

root = Path("public")
# sample up to 50 html files for alt texts near bannerright
alts = Counter()
files = list(root.rglob("*.html"))[:80] + [Path("index.html"), Path("public/immotipp.html")]
for p in files:
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'<img[^>]+bannerright[^>]+>', t):
        tag = m.group(0)
        alt = re.search(r'alt="([^"]*)"', tag)
        if alt:
            alts[alt.group(1)] += 1
    for m in re.finditer(r'<img[^>]+alt="([^"]*)"[^>]+bannerright', t):
        alts[m.group(1)] += 1

for a, c in alts.most_common(30):
    print(c, a)
