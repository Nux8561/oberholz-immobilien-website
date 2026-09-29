from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
detail = (ROOT / "public/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html").read_text(encoding="utf-8", errors="replace")

# Find structural landmarks for cloning/replacing
landmarks = [
    "Charmantes Familienhaus in Krefeld-Linn",
    "5835561",
    "object-hero-780",
    "object-thumb-780",
    "object-thumbnail-780",
    "immo-detail",
    "Kaufpreis",
    "Zimmer",
    "Wohnfläche",
    "Objektbeschreibung",
    "Ausstattung",
    "Lage",
    "Krefeld",
]
for lm in landmarks:
    print(f"{lm!r}: {detail.count(lm)}")

# Extract gallery HTML block between first carousel indicators / thumbs
# Look for repeating thumb pattern
thumbs = re.findall(r'/media/object-thumb-780/5835561_(\d+)\.(jpg|jpeg|png)', detail)
print("thumbs indices", thumbs)

heroes = re.findall(r'/media/object-hero-780/5835561_(\d+)\.(jpg|jpeg|png)', detail)
print("heroes", heroes)

# Find a manageable content section: h1 through description
h1 = detail.find("<h1")
print("h1 pos", h1)
# write a larger middle content extract
# search for main content container
m = re.search(r'<main[^>]*>|id="content"|class="[^"]*object-detail|class="[^"]*immo-detail', detail, re.I)
print("main-ish", m.group(0) if m else None, m.start() if m else None)

# dump all unique path prefixes used for this object
paths = sorted(set(re.findall(r'/media/[^/"\s]+/5835561_[^"\s]+', detail)))
print("media path variants", len(paths))
for p in paths[:40]:
    print(p)
