# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")

# Mobile list block
i = t.find('<li class="my-3 "><a class="" href="/kontakt/immobilienmakler-hamburg.html"')
j = t.find("Immobilienmakler München</a></li>", i)
if j < 0:
    j = t.find("Immobilienmakler M&uuml;nchen</a></li>", i)
print("mobile block", i, j)
if i >= 0 and j >= 0:
    j = j + len("Immobilienmakler München</a></li>")
    Path("scripts/_tmp_mobile_cities.html").write_text(t[i:j], encoding="utf-8")
    print(t[i:j][:500])
    print("...")
    print(t[i:j][-200:])

# Regionen href
m = re.search(r'href="([^"]+)"[^>]*>Unsere Regionen', t)
print("regionen href", m.group(1) if m else None)

# Rotor city mentions?
for needle in ["ocv-rotor", "pillar-card", "Mobilmakler", "bundesweit"]:
    print(needle, t.count(needle))

# Check stuttgart page title for cloning
s = Path("public/kontakt/immobilienmakler-stuttgart.html").read_text(encoding="utf-8", errors="ignore")
title = re.search(r"<title>(.*?)</title>", s)
h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
print("stuttgart title", title.group(1) if title else None)
if h1:
    plain = re.sub(r"<[^>]+>", "", h1.group(1))
    plain = re.sub(r"\s+", " ", plain).strip()
    print("stuttgart h1", plain[:120])
print("Stuttgart count", s.count("Stuttgart"), "stuttgart slug", s.count("stuttgart"))
