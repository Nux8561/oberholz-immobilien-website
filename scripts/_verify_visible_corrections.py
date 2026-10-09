#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

checks = {
    "index": Path("index.html"),
    "leistungen": Path("public/leistungen.html"),
    "bewertung": Path("public/leistungen/immobilienbewertung.html"),
    "energie": Path("public/leistungen/energieberatung.html"),
    "ausweis": Path("public/leistungen/energieausweis-kostenlos.html"),
    "essen_obj": Path(
        "public/immobilien/essen/"
        "eg-wohnung-mit-terrasse-und-garage-barrierefrei-und-bezugsfrei-170647853.html"
    ),
    "essen_makler": Path("public/regionen/essen/immobilienmakler.html"),
}

needles = [
    "bmwi_eneffi",
    "Deutschland machts effizient",
    "BAFA-zertifizierte Energieberater",
    "ard_logo",
    "galileo_logo",
    "logo-rtl",
    "immoscout.png",
    "immobilienbewertung.html",
    "energieberatung.html",
    "energieausweis-kostenlos.html",
    "Energiekompetenz",
    "zertifizierten Immobiliengutachter",
    "Immobilienmakler Bochum",
    "in Bochum und Umgebung",
    "#fde101",
    "bekannt aus",
]

for name, path in checks.items():
    t = path.read_text(encoding="utf-8", errors="ignore")
    print("==", name, path)
    if name == "index":
        print(" TITLE", re.search(r"<title>[^<]+</title>", t).group(0))
        m = re.search(r'name="description"\s+content="([^"]*)"', t)
        if not m:
            m = re.search(r'content="([^"]*)"\s+name="description"', t)
        print(" DESC", (m.group(1)[:200] if m else "n/a"))
    if name in ("bewertung", "energie", "ausweis"):
        print(
            " robots",
            "noindex" in t,
            "stub",
            "nicht an" in t.lower() or "nicht verf" in t.lower(),
        )
    for n in needles:
        c = t.lower().count(n.lower())
        if c:
            print("  HIT", n, c)
    m = re.search(r"Oberholz Immobilien</strong>[^<]{0,220}", t)
    if m:
        print(" FOOTER", m.group(0)[:200])
    print()
