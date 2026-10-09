#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

pages = {
    "index": Path("index.html"),
    "leistungen": Path("public/leistungen.html"),
    "stub_bew": Path("public/leistungen/immobilienbewertung.html"),
    "essen_obj": Path(
        "public/immobilien/essen/"
        "eg-wohnung-mit-terrasse-und-garage-barrierefrei-und-bezugsfrei-170647853.html"
    ),
}

bad = [
    "bmwi_eneffi",
    "Deutschland machts effizient",
    "BAFA-zertifizierte Energieberater",
    "ard_logo",
    "galileo_logo",
    "logo-rtl",
    "immoscout.png",
    "bekannt aus",
    "Energiekompetenz",
    "zertifizierten Immobiliengutachter",
    "DIN-zertifizierten",
    "Energieberatung mit den Oberholz",
    "href=\"/leistungen/immobilienbewertung.html\"",
    "href=\"/leistungen/energieberatung.html\"",
    "href=\"/leistungen/energieausweis-kostenlos.html\"",
]

css = Path("public/theme/oberholz-nav-fix.css").read_text(encoding="utf-8")
print("CSS rainbow override:", ".main-header-scale::after" in css and "background: none !important" in css)

for name, path in pages.items():
    t = path.read_text(encoding="utf-8", errors="ignore")
    hits = [b for b in bad if b.lower() in t.lower()]
    title = re.search(r"<title>[^<]+</title>", t)
    footer = re.search(r"Oberholz Immobilien</strong>[^<]{0,160}", t)
    print(f"\n== {name}")
    print(" title", title.group(0) if title else None)
    print(" footer", footer.group(0)[:160] if footer else None)
    print(" bad_hits", hits or "none")
    if name.startswith("stub"):
        print(" stub_ok", "noindex" in t and "nicht an" in t.lower())
