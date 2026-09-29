from pathlib import Path
import re
from collections import Counter

ROOT = Path(".")

# Unique Service-PIN markup patterns
pin_re = re.compile(
    r'<div class="text-center d-block">\s*'
    r'<span class="text-muted">Service-PIN:\s*'
    r'<strong class="text-md"[^>]*>[^<]+</strong>\s*'
    r'</span>\s*</div>',
    re.I,
)

# Count leftover foreign names / images in felde + sample
names = [
    "Ute Schorpp",
    "Wolfgang Mayer",
    "Kersten Streit",
    "Axel Winkler",
    "René Mohr",
    "Rene Mohr",
    "Christian Munz",
    "profilbild_winkler",
    "streit_facepile",
    "Service-PIN",
]

print("--- Felde leftover counts ---")
for p in Path("public/regionen/felde").rglob("*.html"):
    t = p.read_text(encoding="utf-8", errors="replace")
    print(p.name)
    for n in names:
        c = t.count(n)
        if c:
            print(f"  {n}: {c}")

# List media facepile files
fp = Path("public/media/facepile")
print("\nfacepile files:", sorted(x.name for x in fp.glob("*")) if fp.exists() else "missing")

# Check which bannerright folders exist for t7a7913
print("\nbannerright with t7a7913:")
for d in sorted(Path("public/media").glob("bannerright-*")):
    hits = list(d.glob("t7a7913*"))
    if hits:
        print(d.name, [h.name for h in hits])

# Sample PIN variants count via quick scan of a few cities
print("\nPIN samples:")
seen = Counter()
for city in Path("public/regionen").iterdir():
    if not city.is_dir():
        continue
    for p in city.glob("*.html"):
        t = p.read_text(encoding="utf-8", errors="replace")
        for m in pin_re.finditer(t):
            seen[m.group(0)[:80]] += 1
        if sum(seen.values()) > 20:
            break
    if sum(seen.values()) > 20:
        break
for k, v in seen.most_common(5):
    print(v, repr(k))
