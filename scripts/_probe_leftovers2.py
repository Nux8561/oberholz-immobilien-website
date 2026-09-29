from pathlib import Path
import re
from collections import Counter

ROOT = Path(".")
SKIP = {"node_modules", ".git", "dist", "assets"}

# Count leftover names across a sample + priority
leftover_names = Counter()
pin_files = 0
pin_codes = Counter()
facepile_refs = Counter()
ute_context = []

pin_code_re = re.compile(r"Service-PIN:.*?>([A-Z0-9]+)<", re.S)
face_re = re.compile(r"/media/facepile/([a-z0-9_\.-]+)", re.I)

# Only scan priority + felde + a few cities for speed; then count pins via walking regionen names only on *.html one level
priority = [
    Path("index.html"),
    *Path("public").glob("*.html"),
    Path("public/regionen/felde"),
    Path("public/regionen/muenster"),
    Path("public/regionen/essen"),
    Path("public/immobilien"),
]

files = []
for p in priority:
    if p.is_file():
        files.append(p)
    elif p.is_dir():
        files.extend(p.rglob("*.html"))

names = [
    "Ute Schorpp",
    "Wolfgang Mayer",
    "Kersten Streit",
    "Axel Winkler",
    "René Mohr",
    "Rene Mohr",
    "Christian Munz",
    "Michael Penn",
    "profilbild_winkler",
    "profilbild_mayer",
    "team_mohr",
    "munz_ie",
    "streit_facepile",
]

print("scanned", len(files))
for p in files:
    t = p.read_text(encoding="utf-8", errors="replace")
    if "Service-PIN" in t:
        pin_files += 1
        for m in pin_code_re.finditer(t):
            pin_codes[m.group(1)] += 1
    for n in names:
        c = t.count(n)
        if c:
            leftover_names[n] += c
    for m in face_re.finditer(t):
        facepile_refs[m.group(1)] += 1
    if "Ute Schorpp" in t and len(ute_context) < 3:
        i = t.find("Ute Schorpp")
        ute_context.append((str(p), t[max(0, i - 80) : i + 100]))

print("pin_files", pin_files, "codes", pin_codes.most_common(10))
print("leftover", leftover_names)
print("facepile refs", facepile_refs)
for p, ctx in ute_context:
    print("UTE", p, repr(ctx))

# list team / contact / avatar dirs
for dname in ["team", "videocard_avatar", "immobilien-contact-card", "pillar-card", "headbanner-testimonials"]:
    d = Path("public/media") / dname
    if d.exists():
        files2 = sorted(x.name for x in d.iterdir() if x.is_file())[:30]
        print(dname, len(list(d.iterdir())), "sample", files2)
