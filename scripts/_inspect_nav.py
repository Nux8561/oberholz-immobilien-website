#!/usr/bin/env python3
"""Extract nav + buy-related links from core pages."""
from pathlib import Path
import re

html = Path("index.html").read_text(encoding="utf-8", errors="replace")

print("=== NAV STANDORTE ===")
for m in re.finditer(r'href="(/kontakt/immobilienmakler-[^"]+)"[^>]*>([^<]{0,60})', html):
    print(m.group(1), "|", m.group(2).strip())

print("\n=== LEISTUNGEN LINKS ===")
for m in re.finditer(r'href="(/leistungen/[^"]+)"[^>]*>([^<]{0,80})', html):
    print(m.group(1), "|", m.group(2).strip())

print("\n=== kaufen / Mehrfamilien mentions (index) ===")
for kw in ["Mehrfamilien", "Wohnungen kaufen", "Wohnung kaufen", "Immobilie kaufen", "Kapitalanlage"]:
    print(kw, html.count(kw))

# check if dedicated pages exist
print("\n=== candidate pages ===")
for p in Path("public").rglob("*.html"):
    if any(x in p.parts for x in ("regionen", "immopedia", "immobilien")):
        continue
    name = p.name.lower()
    if any(k in name for k in ("kauf", "mehrfamilien", "wohnung", "kapital")):
        print(p)
