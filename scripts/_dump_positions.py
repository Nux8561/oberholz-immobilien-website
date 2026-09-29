# -*- coding: utf-8 -*-
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")
positions = [39816, 53309, 111279]
for pos in positions:
    Path(f"scripts/_tmp_pos_{pos}.html").write_text(t[pos - 200 : pos + 1800], encoding="utf-8")
    print("===", pos, "===")
    print(t[pos - 100 : pos + 200].replace("\n", " ")[:300])
    print()

# Save full table via simpler find
i = t.find('<div class="table-responsive">')
# find the one near Standorte
j = t.find("Unsere Standorte in")
i = t.find('<div class="table-responsive">', j)
k = t.find("</table>", i) + len("</table>")
# include closing div
k2 = t.find("</div>", k) + len("</div>")
table = t[i:k2]
Path("scripts/_tmp_standorte_table.html").write_text(table, encoding="utf-8")
print("table saved", len(table), "rows", table.count("<tr>"))
