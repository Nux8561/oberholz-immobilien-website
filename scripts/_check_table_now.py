# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")
j = t.find("Unsere Standorte")
chunk = t[j : j + 10000]
Path("scripts/_tmp_table_now.html").write_text(chunk, encoding="utf-8")
# extract row labels
for m in re.finditer(r"<tr>(.*?)</tr>", chunk, re.S):
    plain = re.sub(r"<[^>]+>", " ", m.group(1))
    plain = re.sub(r"\s+", " ", plain).strip()
    if plain and "Zuständig" not in plain:
        print("ROW:", plain[:160])

print("\n--- leftovers context ---")
for needle in ["Hamburg", "Baden-Württemberg", "bundesweit", "Berlin", "Augsburg", "Nürnberg", "München", "Stuttgart"]:
    i = t.find(needle)
    if i >= 0:
        ctx = t[max(0, i - 60) : i + 80]
        print(needle, "=>", re.sub(r"\s+", " ", ctx))
