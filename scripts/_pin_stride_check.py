from pathlib import Path

regionen = Path("public/regionen")
cities = sorted(d for d in regionen.iterdir() if d.is_dir())
hits = []
checked = 0
# every 40th city + all public root
for city in cities[::40]:
    for p in city.glob("*.html"):
        checked += 1
        try:
            if b"Service-PIN" in p.read_bytes():
                hits.append(str(p))
        except OSError:
            pass

root_hits = []
for p in Path("public").glob("*.html"):
    checked += 1
    try:
        if b"Service-PIN" in p.read_bytes():
            root_hits.append(p.name)
    except OSError:
        pass
idx = Path("index.html")
if idx.exists():
    checked += 1
    if b"Service-PIN" in idx.read_bytes():
        root_hits.append("index.html")

print("checked", checked, "region_hits", len(hits), "root_hits", root_hits[:10])
for h in hits[:12]:
    print(h)
