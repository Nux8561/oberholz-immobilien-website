from pathlib import Path
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Wrong locations that should not be Oberholz hubs
BAD = [
    "Stuttgart",
    "Villingen",
    "Schwenningen",
    "Frankfurt",
    "München",
    "Munchen",
    "Hamburg",
    "Hannover",
    "Düsseldorf",
    "Duesseldorf",
]

files = [Path("index.html")]
files += list(Path("public").rglob("*.html"))

# Fast scan: count files with bad location terms in nav/kontakt context
hit_files = Counter()
term_files = Counter()
examples = []

for p in files:
    try:
        raw = p.read_bytes()
    except OSError:
        continue
    # skip if none of bad terms as bytes
    if not any(t.encode() in raw for t in ["Stuttgart", "Villingen", "Frankfurt", "München", "Hamburg", "Hannover", "Düsseldorf", "Duesseldorf", "Schwenningen"]):
        continue
    t = raw.decode("utf-8", errors="ignore")
    for term in BAD:
        if term in t:
            term_files[term] += 1
    hit_files[str(p.as_posix())] = sum(t.count(x) for x in BAD)
    if len(examples) < 25:
        examples.append((p.as_posix(), {x: t.count(x) for x in BAD if t.count(x)}))

print("files with bad locs", len(hit_files))
print("term file counts", dict(term_files))
print("\nTOP files")
for f, n in hit_files.most_common(20):
    print(n, f)

# Inspect kontakt dropdown in index
t = Path("index.html").read_text(encoding="utf-8", errors="ignore")
i = t.find('title="Kontakt"')
print("\nKONTAKT NAV snippet:")
chunk = t[i:i+3500]
# extract location links
for m in re.finditer(r'href="([^"]*kontakt[^"]*)"[^>]*>(.*?)</a>', chunk, re.I|re.S):
    plain = re.sub(r'<[^>]+>',' ', m.group(2))
    plain = re.sub(r'\s+',' ', plain).strip()
    if plain:
        print("-", m.group(1), "=>", plain[:80])
