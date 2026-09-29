"""Precise img-tag pairing: banner filename <-> alt person name."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PERSON_RE = re.compile(
    r"(Michael Oberholz|Felix Lesch|Michael Penn|Pascal Kopp|Lubka Röger|"
    r"Kersten Streit|Wolfgang Mayer|Axel Winkler|René Mohr|Rene Mohr|"
    r"Christian Munz|Ute Schorpp)"
)

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
SRC_RE = re.compile(r'\bsrc="([^"]+)"', re.I)
ALT_RE = re.compile(r'\balt="([^"]*)"', re.I)
BANNER_RE = re.compile(r"bannerright-\d+/(t7a[a-z0-9_.]+\.png)", re.I)

files: list[Path] = [ROOT / "index.html"]
files.extend((ROOT / "public").glob("*.html"))
# Sample ~40 region cities alphabetically + felde
regionen = ROOT / "public" / "regionen"
cities = sorted([d for d in regionen.iterdir() if d.is_dir()]) if regionen.exists() else []
# include felde explicitly + every 150th city for breadth + first 80
pick = set()
for d in cities[:80]:
    pick.add(d)
for d in cities[::150]:
    pick.add(d)
for name in ("felde", "muenster", "essen", "bochum", "dortmund"):
    d = regionen / name
    if d.exists():
        pick.add(d)
for d in pick:
    files.extend(d.glob("*.html"))

pair: dict[str, Counter] = defaultdict(Counter)
for path in files:
    text = path.read_text(encoding="utf-8", errors="replace")
    for tag in IMG_RE.findall(text):
        src_m = SRC_RE.search(tag)
        alt_m = ALT_RE.search(tag)
        if not src_m or not alt_m:
            continue
        bm = BANNER_RE.search(src_m.group(1))
        if not bm:
            continue
        nm = PERSON_RE.search(alt_m.group(1))
        if nm:
            pair[bm.group(1).lower()][nm.group(1)] += 1

lines = [f"files={len(files)}", "IMG ALT ONLY:"]
mapping = {}
for fn, c in sorted(pair.items()):
    top = c.most_common()
    lines.append(f"  {fn}: {top}")
    if top:
        mapping[fn] = top[0][0]

# Map person → team image
PERSON_TO_FILE = {
    "Michael Oberholz": "michael-oberholz.png",
    "Kersten Streit": "michael-oberholz.png",
    "Felix Lesch": "felix-lesch.png",
    "Wolfgang Mayer": "felix-lesch.png",
    "Michael Penn": "michael-penn.png",
    "Axel Winkler": "michael-penn.png",
    "Pascal Kopp": "pascal-kopp.png",
    "René Mohr": "pascal-kopp.png",
    "Rene Mohr": "pascal-kopp.png",
    "Lubka Röger": "lubka-roeger.png",
    "Christian Munz": "lubka-roeger.png",
    "Ute Schorpp": "lubka-roeger.png",
}

lines.append("")
lines.append("CORRECT overwrite map (banner file → team png):")
for fn, person in sorted(mapping.items()):
    team = PERSON_TO_FILE[person]
    lines.append(f'  "{fn}": "{team}",  # {person}')

out = ROOT / "scripts" / "_banner_alt_map.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
