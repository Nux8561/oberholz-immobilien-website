#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("public/theme/contact-widget.html").read_text(encoding="utf-8")

needles = [
    "14.700",
    "14.000",
    "14700",
    "Kunden",
    "dena",
    "BAFA",
    "20 Jahre",
    "Jahre Erfahrung",
    "zertifiziert",
    "cw-badge",
    "sticky-support",
    "sticky-kontakt",
    "sticky-anfrage",
]

for n in needles:
    print("===", n, t.count(n))

# extract badge / sticky sections
for sid in ["sticky-support", "sticky-kontakt", "sticky-anfrage", "sticky-anrufen", "sticky-rueckruf", "sticky-whatsapp"]:
    i = t.find(f'id="{sid}"')
    if i < 0:
        print("missing", sid)
        continue
    Path(f"scripts/_cw_{sid}.txt").write_text(t[i : i + 1800], encoding="utf-8")
    print("wrote", sid)

# also find all badge-row blocks
for i, m in enumerate(re.finditer(r'class="cw-badge-row"[\s\S]{0,600}', t)):
    Path(f"scripts/_cw_badge_row_{i}.txt").write_text(m.group(0), encoding="utf-8")
    print("badge", i, m.group(0)[:120].replace("\n", " "))
