# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/service/finanzierungsrechner.html").read_text(encoding="utf-8", errors="ignore")
m = re.search(
    r"(<h2>\s*Grunderwerbsteuer nach Bundesland</h2>.*?<div class=\"table-responsive\">.*?</table>\s*</div>)",
    t,
    re.S,
)
print("found", bool(m))
if m:
    Path("scripts/_tmp_broken_grest.html").write_text(m.group(1), encoding="utf-8")
    print("len", len(m.group(1)))

# Find JS rates map
for pat in [
    r"GREST[^\n]{0,200}",
    r"grEst[^\n]{0,200}",
    r"BW\s*:\s*[\d.]+",
    r"'BW'\s*:\s*[\d.]+",
    r'"BW"\s*:\s*[\d.]+',
    r"Baden-Württemberg[^\n]{0,80}",
]:
    ms = list(re.finditer(pat, t))
    print(pat, "hits", len(ms))
    for x in ms[:3]:
        print(" ", x.group(0)[:180])

# Look for rates near calculator script
idx = t.find("const rates") 
if idx < 0:
    idx = t.find("var rates")
if idx < 0:
    idx = t.find("grunderwerb")
print("grunderwerb idx samples:")
for m in re.finditer(r".{0,40}grunderwerb.{0,80}", t, re.I):
    print(re.sub(r"\s+", " ", m.group(0))[:140])
    if m.start() > 200000:
        break
