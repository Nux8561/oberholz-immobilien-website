# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")

# Extract full mega-menu block for Kontakt - look for the column with city links
# Pattern around hamburg link
needle = "/kontakt/immobilienmakler-hamburg.html"
i = t.find(needle)
print("first hamburg at", i)
# go back to find parent ul/div
start = t.rfind("<div", max(0, i - 2000), i)
# find a better marker
for marker in ["Unsere Regionen", "Standorte", "Mobil", "dropdown-menu", "mega-menu", "col-lg"]:
    j = t.rfind(marker, max(0, i - 3000), i)
    print("marker", marker, j)

# dump 2500 chars before first city link in nav area (first occurrence after title=Kontakt)
nav_start = t.find('title="Kontakt"')
nav_city = t.find("/kontakt/immobilienmakler-hamburg.html", nav_start)
print("nav city", nav_city)
block = t[nav_city - 800 : nav_city + 2500]
Path("scripts/_tmp_nav_cities.html").write_text(block, encoding="utf-8")
print(block[:500])
print("---")
print(block[-500:])

# standort cards section
card_i = t.find("Externer Link Icon Immobilienmakler Stuttgart")
print("\ncard at", card_i)
cards = t[card_i - 1500 : card_i + 4000]
Path("scripts/_tmp_cards.html").write_text(cards, encoding="utf-8")
