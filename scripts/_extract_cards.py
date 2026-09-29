# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")

# Find standort card section via href
for city in ["stuttgart", "duesseldorf", "hannover", "hamburg"]:
    href = f"/kontakt/immobilienmakler-{city if city != 'duesseldorf' else 'duesseldorf'}.html"
    # fix hamburg
    if city == "hamburg":
        href = "/kontakt/immobilienmakler-hamburg.html"
    elif city == "stuttgart":
        href = "/kontakt/immobilienmakler-stuttgart.html"
    elif city == "duesseldorf":
        href = "/kontakt/immobilienmakler-duesseldorf.html"
    elif city == "hannover":
        href = "/kontakt/immobilienmakler-hannover.html"
    i = t.find(href)
    print(city, "href count", t.count(href), "first", i)

# Find section around "Unsere Standorte in"
i = t.find("Unsere Standorte in")
print("heading at", i)
Path("scripts/_tmp_cards2.html").write_text(t[i:i+15000], encoding="utf-8")

# mobile menu cities
mi = t.find('id="mobileMenu"')
print("mobileMenu", mi)
# search for immobilienmakler in mobile area
chunk = t[mi:mi+80000] if mi > 0 else ""
cities_m = re.findall(r'immobilienmakler-[a-z-]+\.html', chunk)
print("mobile city links unique", sorted(set(cities_m))[:20], "count", len(cities_m))

# Also check footer Unsere Regionen
fi = t.find("Unsere Regionen")
print("Unsere Regionen", fi)
if fi > 0:
    Path("scripts/_tmp_regionen.html").write_text(t[fi:fi+5000], encoding="utf-8")
