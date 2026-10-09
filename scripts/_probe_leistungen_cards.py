#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
t = Path("public/leistungen.html").read_text(encoding="utf-8", errors="ignore")
for pat in [
    "immobilienbewertung",
    "energieberatung",
    "energieausweis",
    "Energiekompetenz",
    "Gutachter",
    "BAFA",
    "bmwi",
    "immoscout",
    "bekannt aus",
    "Essen und Umgebung",
    "Bochum und Umgebung",
]:
    print(pat, t.lower().count(pat.lower()))

m = re.search(r"Oberholz Immobilien</strong>[^<]{0,250}", t)
print("FOOTER", m.group(0) if m else None)

# list service hrefs still present
hrefs = sorted(set(re.findall(r'href="(/leistungen/[^"]+)"', t)))
print("HREFS", hrefs)
