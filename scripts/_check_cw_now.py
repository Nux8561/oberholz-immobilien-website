#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("index.html").read_text(encoding="utf-8")
print("Lokale Ansicht", t.count("Lokale Ansicht"))
print("cw-local-overlay", t.count("cw-local-overlay"))
print("pages.dev", t.count("pages.dev"))
print("profilbild_mayer", t.count("profilbild_mayer"))
print("oberholz_facepile", t.count("oberholz_facepile"))
print("Felix Lesch", t.count("Felix Lesch"))
print("Michael Oberholz face", "oberholz_facepile" in t or "michael-oberholz" in t.lower())

i = t.find('id="cw-trigger"')
print("--- trigger ---")
print(t[i : i + 500] if i >= 0 else "missing")

i = t.find("Lokale Ansicht")
print("--- lokale ---")
print(t[i - 100 : i + 180] if i >= 0 else "gone")

i = t.find("cw-local-overlay")
print("--- overlay stub ---")
print(t[i : i + 400] if i >= 0 else "missing")

# how many core files still have Lokale Ansicht
n = 0
for p in [Path("index.html"), *Path("public").glob("*.html"), *Path("public/leistungen").glob("*.html")]:
    if "Lokale Ansicht" in p.read_text(encoding="utf-8", errors="replace"):
        n += 1
        print("still", p)
print("files with Lokale", n)

# facepile media
media = Path("public/media")
for pat in ["*face*", "*profil*", "*mayer*", "*lesch*", "*oberholz*"]:
    for p in media.rglob(pat):
        print("media", p.relative_to(media))
