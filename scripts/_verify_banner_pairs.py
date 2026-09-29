"""Map each banner portrait file to the person name used next to it in HTML."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAME_RE = re.compile(
    r"(Michael Oberholz|Felix Lesch|Michael Penn|Pascal Kopp|Lubka Röger|"
    r"Kersten Streit|Wolfgang Mayer|Axel Winkler|René Mohr|Rene Mohr|"
    r"Christian Munz|Ute Schorpp)"
)

FNAMES = [
    "t7a0115_kopie.png",
    "t7a3306.png",
    "t7a3373.png",
    "t7a3420.png",
    "t7a7869.png",
    "t7a7897.png",
    "t7a7913_1.png",
    "t7a9283_kopie.png",
    "t7a9489_copy.png",
]

# Expected after correct name mapping from old EE people
# Cycle used in replace_foreign_portraits (WRONG if not aligned with names):
CYCLE = {
    "t7a0115_kopie.png": "Michael Oberholz",
    "t7a3306.png": "Felix Lesch",
    "t7a3373.png": "Michael Penn",
    "t7a3420.png": "Pascal Kopp",
    "t7a7869.png": "Lubka Röger",
    "t7a7897.png": "Michael Oberholz",
    "t7a7913_1.png": "Felix Lesch",
    "t7a9283_kopie.png": "Michael Penn",
    "t7a9489_copy.png": "Pascal Kopp",
}

files: list[Path] = [ROOT / "index.html"]
files.extend((ROOT / "public").glob("*.html"))
for city in [
    "felde",
    "muenster",
    "essen",
    "bochum",
    "dortmund",
    "koeln",
    "bielefeld",
    "aachen",
    "gelsenkirchen",
]:
    d = ROOT / "public" / "regionen" / city
    if d.exists():
        files.extend(d.glob("*.html"))

pair = defaultdict(Counter)
for path in files:
    text = path.read_text(encoding="utf-8", errors="replace")
    for fn in FNAMES:
        for m in re.finditer(re.escape(fn), text):
            ctx = text[m.start() : m.start() + 500]
            for nm in NAME_RE.finditer(ctx):
                pair[fn][nm.group(1)] += 1

lines = [
    f"scanned_files={len(files)}",
    "",
    "Banner file → most common nearby name vs cycle overwrite:",
]
mismatches = []
for fn in FNAMES:
    top = pair[fn].most_common(3)
    expected_cycle = CYCLE[fn]
    dominant = top[0][0] if top else None
    ok = dominant == expected_cycle if dominant else "?"
    lines.append(f"  {fn}")
    lines.append(f"    cycle_image_is: {expected_cycle}")
    lines.append(f"    html_nearby:    {top}")
    lines.append(f"    match: {ok}")
    if dominant and dominant != expected_cycle:
        mismatches.append((fn, expected_cycle, dominant))

lines.append("")
lines.append(f"MISMATCHES: {len(mismatches)}")
for item in mismatches:
    lines.append(f"  {item}")

# Facepile path mapping (by old filename semantics — reliable)
lines.append("")
lines.append("Facepile filename semantics (reliable):")
lines.append("  profilbild_winkler → Michael Penn (ex Axel Winkler)")
lines.append("  profilbild_mayer   → Felix Lesch (ex Wolfgang Mayer)")
lines.append("  streit_facepile    → Michael Oberholz (ex Kersten Streit)")
lines.append("  team_mohr          → Pascal Kopp (ex René Mohr)")
lines.append("  munz_ie            → Lubka Röger (ex Christian Munz)")
lines.append("  team_schorpp/Ute   → Lubka Röger")

out = ROOT / "scripts" / "_banner_name_pairs.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
