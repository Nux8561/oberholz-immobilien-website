#!/usr/bin/env python3
from pathlib import Path
import re

files = [Path("index.html")]
files += list(Path("public").glob("*.html"))
files += list(Path("public/leistungen").glob("*.html"))
files += list(Path("public/ueber-uns").glob("*.html"))
files += list(Path("public/service").glob("*.html"))
files += list(Path("public/kontakt").glob("*.html"))
print("files", len(files))
needles = {
    "dvag": "dvag-logo",
    "wue": "wuestenrot",
    "flow": "flowfact",
    "klein": "kleinanzeigen",
    "immowelt": "immowelt.png",
    "32697": "32697_3_3",
    "swiss": "swiss-life",
    "interhyp": "interhyp-logo",
    "galileo link": "galileo.tv",
    "sat1 link": "sat1.de",
}
for label, needle in needles.items():
    n = sum(1 for f in files if needle.lower() in f.read_text(encoding="utf-8", errors="replace").lower())
    print(label, n)

print("--- titles ---")
for f in [
    Path("index.html"),
    Path("public/leistungen.html"),
    Path("public/immobilien.html"),
    Path("public/ueber-uns.html"),
    Path("public/kontakt/immobilienmakler-bochum.html"),
    Path("public/service/kann-ich-kaufen.html"),
]:
    t = f.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<title>([^<]+)</title>", t)
    d = re.search(r'name="description" content="([^"]+)"', t)
    if not d:
        d = re.search(r'content="([^"]+)" name="description"', t)
    print(f.name, "|", m.group(1) if m else "?", "|", (d.group(1)[:120] if d else "?"))

# partner block sample
t = Path("index.html").read_text(encoding="utf-8", errors="replace")
i = t.find("partner-section")
print("--- partner ---")
print(t[i : i + 700] if i >= 0 else "missing")
i = t.lower().find("bekannt aus")
print("--- trust ---")
print(t[i : i + 900] if i >= 0 else "missing")
