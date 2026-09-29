# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")

# Full standorte table
m = re.search(
    r'(<div class="table-responsive">\s*<table class="table table-hover border align-middle">.*?</table>\s*</div>)',
    t,
    re.S,
)
if m:
    Path("scripts/_tmp_standorte_table.html").write_text(m.group(1), encoding="utf-8")
    print("table len", len(m.group(1)))
    print("rows", m.group(1).count("<tr>"))
else:
    print("no table")

# Mobile Kontakt accordion items with cities
# find all <a ... immobilienmakler-... in mobile menu section between mobileMenu and end of nav-ish
mi = t.find('id="mobileMenu"')
# find Kontakt collapse
for label in ["Hamburg", "Stuttgart", "München", "Villingen"]:
    pass

# Extract mobile kontakt list - look for pattern with ocv-rotor or accordion
idx = t.find(">Kontakt aufnehmen</")
print("Kontakt aufnehmen text", t.count("Kontakt aufnehmen"))

# Find second occurrence areas - desktop + mobile
positions = [m.start() for m in re.finditer(r'immobilienmakler-hamburg\.html', t)]
print("hamburg positions", positions)

# Dump mobile menu kontakt city links context
# Search for accordion-body near Kontakt
for m in re.finditer(r'id="(Kontakt|kontakt)[^"]*"', t):
    print("id match", m.group(0), m.start())

# Try data-bs-parent
for m in re.finditer(r'data-bs-parent="#[^"]*[Kk]ontakt[^"]*"', t):
    print("parent", m.group(0), m.start())

# Look at footer regionen
fi = t.find("Unsere Regionen")
chunk = t[fi:fi+3000]
Path("scripts/_tmp_regionen.html").write_text(chunk, encoding="utf-8")
print("regionen preview", re.sub(r"\s+", " ", chunk)[:500])
