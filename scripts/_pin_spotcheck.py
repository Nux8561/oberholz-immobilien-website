from pathlib import Path

regionen = Path("public/regionen")
cities = sorted(d for d in regionen.iterdir() if d.is_dir())
# Check a few cities from the end of alphabet + around where abort happened (~3600+)
samples = []
# last 20 cities
for city in cities[-20:]:
    samples.append(city)
# around index 4000, 5000, 6000
for idx in (4000, 5000, 6000, 6500):
    if idx < len(cities):
        samples.append(cities[idx])
# also felde
felde = regionen / "felde"
if felde.exists():
    samples.append(felde)

hits = []
clean = 0
for city in samples:
    for p in city.glob("*.html"):
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        if b"Service-PIN" in raw:
            hits.append(str(p.relative_to(Path("."))))
        else:
            clean += 1

print("sampled_files", clean + len(hits), "with_pin", len(hits), "clean", clean)
for h in hits[:15]:
    print("PIN", h)
