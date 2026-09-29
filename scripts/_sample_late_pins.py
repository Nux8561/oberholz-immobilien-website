from pathlib import Path

regionen = Path("public/regionen")
cities = sorted(d for d in regionen.iterdir() if d.is_dir())
# sample late cities for remaining PIN
hits = []
checked = 0
for city in cities[4000:]:
    for p in city.glob("*.html"):
        checked += 1
        raw = p.read_bytes()
        if b"Service-PIN" in raw:
            hits.append(str(p))
            if len(hits) >= 8:
                break
    if len(hits) >= 8:
        break
print("checked", checked, "hits", len(hits))
for h in hits:
    print(h)
