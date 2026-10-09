# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")
print("module-3355", "module-3355" in t)
print("Steuersatz", t.count("Steuersatz"))
print("Bundesland th-ish", len(re.findall(r">Bundesland<", t)))
print("standorte-table", "standorte-table" in t)
print("Essen und Ruhrgebiet", t.count("Essen und Ruhrgebiet"))
print("table-striped", t.count("table-striped"))
print("table-bordered", t.count("table-bordered"))

for m in re.finditer(r'id="module-(\d+)"', t):
    print("module", m.group(1), "at", m.start())

for m in re.finditer(r"<th[^>]*>(.*?)</th>", t, re.S):
    plain = re.sub(r"<[^>]+>", "", m.group(1))
    plain = re.sub(r"\s+", " ", plain).strip()
    if plain:
        print("TH:", plain[:100])

# Find fliesstext / table-responsive blocks
for m in re.finditer(r'id="module-\d+"[^>]*>|class="[^"]*fliesstext[^"]*"', t):
    pass

idx = t.find("Steuersatz")
if idx >= 0:
    print("Steuer ctx:", re.sub(r"\s+", " ", t[idx - 200 : idx + 400]))

idx2 = t.find("Essen und Ruhrgebiet")
if idx2 >= 0:
    print("Essen ctx:", re.sub(r"\s+", " ", t[max(0, idx2 - 300) : idx2 + 200]))
