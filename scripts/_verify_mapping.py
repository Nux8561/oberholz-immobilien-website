"""Verify portrait filename slots map to the same Oberholz person as HTML names."""
from pathlib import Path
from PIL import Image
import hashlib

ROOT = Path(__file__).resolve().parents[1]
TEAM = ROOT / "public" / "media" / "oberholz-team"
MEDIA = ROOT / "public" / "media"

# Expected: old EE slot → Oberholz person (same as replace_foreign_portraits TEAM cycle)
BANNER_ORDER = [
    ("t7a0115_kopie.png", "michael-oberholz.png", "Michael Oberholz"),
    ("t7a3306.png", "felix-lesch.png", "Felix Lesch"),
    ("t7a3373.png", "michael-penn.png", "Michael Penn"),
    ("t7a3420.png", "pascal-kopp.png", "Pascal Kopp"),
    ("t7a7869.png", "lubka-roeger.png", "Lubka Röger"),
    ("t7a7897.png", "michael-oberholz.png", "Michael Oberholz"),
    ("t7a7913_1.png", "felix-lesch.png", "Felix Lesch"),
    ("t7a9283_kopie.png", "michael-penn.png", "Michael Penn"),
    ("t7a9489_copy.png", "pascal-kopp.png", "Pascal Kopp"),
]

FACEPILE = [
    ("facepile/profilbild_winkler.jpg", "michael-penn.png", "Michael Penn", "was Axel Winkler"),
    ("facepile/profilbild_mayer.jpg", "felix-lesch.png", "Felix Lesch", "was Wolfgang Mayer"),
    ("facepile/streit_facepile.jpg", "michael-oberholz.png", "Michael Oberholz", "was Kersten Streit"),
    ("facepile/team_mohr.jpg", "pascal-kopp.png", "Pascal Kopp", "was René Mohr"),
    ("facepile/munz_ie.png", "lubka-roeger.png", "Lubka Röger", "was Christian Munz"),
    ("team/lubka-roeger.jpg", "lubka-roeger.png", "Lubka Röger", "was Ute Schorpp slot"),
    ("team/team_schorpp.jpg", "lubka-roeger.png", "Lubka Röger", "was Ute Schorpp"),
]

NAME_MAP = [
    ("Kersten Streit", "Michael Oberholz"),
    ("Wolfgang Mayer", "Felix Lesch"),
    ("Axel Winkler", "Michael Penn"),
    ("René Mohr / Rene Mohr", "Pascal Kopp"),
    ("Christian Munz", "Lubka Röger"),
    ("Ute Schorpp", "Lubka Röger"),
]


def file_sig(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    data = path.read_bytes()
    return f"{len(data)}:{hashlib.md5(data).hexdigest()[:10]}"


def team_resized_sig(team_file: str, dest: Path) -> str:
    """Rough check: dest should resemble team source (not identical due to resize/JPEG)."""
    src = TEAM / team_file
    if not src.exists() or not dest.exists():
        return "skip"
    # Compare aspect / that dest is not tiny broken
    im = Image.open(dest)
    return f"ok {im.size} mode={im.mode}"


lines = []
lines.append("=== NAME MAPPING (old → Oberholz) ===")
for a, b in NAME_MAP:
    lines.append(f"  {a}  →  {b}")

lines.append("\n=== BANNER SLOT ORDER (idx % 5 team cycle) ===")
for fname, team, person in BANNER_ORDER:
    dest = MEDIA / "bannerright-780" / fname
    lines.append(f"  {fname} → {person} ({team}) exists={dest.exists()} {team_resized_sig(team, dest)}")

lines.append("\n=== FACEPILE / TEAM FILES ===")
for rel, team, person, note in FACEPILE:
    dest = MEDIA / rel
    lines.append(f"  {rel} → {person} ({note}) {team_resized_sig(team, dest)}")

# Spot-check Felde HTML: which banner files sit next to which alt names
import re
felde = ROOT / "public/regionen/felde/immobilienmakler.html"
if felde.exists():
    t = felde.read_text(encoding="utf-8", errors="replace")
    lines.append("\n=== FELDE immobilienmakler: img src+alt (portrait-ish) ===")
    for m in re.finditer(r'<img[^>]+>', t):
        tag = m.group(0)
        if not any(k in tag for k in ("bannerright", "facepile", "team/", "avatar")):
            continue
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if src:
            lines.append(f"  {src.group(1)} | {alt.group(1) if alt else ''}")

# Check consistency: t7a7913 should be Felix if cycle is correct; Felde had Michael Penn with t7a7913
# That would be a MISMATCH if alt says Penn but file is Felix!
lines.append("\n=== CONSISTENCY NOTE ===")
lines.append("Banner cycle idx: t7a7913_1 = index 6 → Felix Lesch")
lines.append("Name replace: Axel Winkler → Michael Penn (often paired with winkler/t7a3373 or similar)")
lines.append("If HTML alt says Penn next to t7a7913_1.png, alt/file can disagree — need fix.")

(ROOT / "scripts/_mapping_report.txt").write_text("\n".join(lines), encoding="utf-8")
print("wrote scripts/_mapping_report.txt", len(lines), "lines")
