# -*- coding: utf-8 -*-
"""Restore Grunderwerbsteuer table on finanzierungsrechner (corrupted by standorte tbody replace)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "public" / "service" / "finanzierungsrechner.html"

# Same rates as const STATES in the page script (display names for NRW)
RATES = [
    ("Baden-Württemberg", "5,0 %"),
    ("Bayern", "3,5 %"),
    ("Berlin", "6,0 %"),
    ("Brandenburg", "6,5 %"),
    ("Bremen", "5,0 %"),
    ("Hamburg", "5,5 %"),
    ("Hessen", "6,0 %"),
    ("Mecklenburg-Vorpommern", "6,0 %"),
    ("Niedersachsen", "5,0 %"),
    ("Nordrhein-Westfalen", "6,5 %"),
    ("Rheinland-Pfalz", "5,0 %"),
    ("Saarland", "6,5 %"),
    ("Sachsen", "5,5 %"),
    ("Sachsen-Anhalt", "5,0 %"),
    ("Schleswig-Holstein", "6,5 %"),
    ("Thüringen", "5,0 %"),
]

ROWS = "".join(
    f"<tr> <td>{name}</td> <td class=\"text-end\">{rate}</td> </tr>"
    for name, rate in RATES
)

NEW_TABLE = (
    '<div class="table-responsive"><table class="table table-hover align-middle mb-0 '
    'table-striped table-bordered"> <thead class="table-light"> <tr> '
    '<th scope="col">Bundesland</th> '
    '<th scope="col" class="text-end">Steuersatz</th> '
    "</tr> </thead> <tbody> "
    f"{ROWS}"
    " </tbody> "
    '<caption class="pt-2 text-body-secondary"> Hinweis: Die GrESt-Sätze können sich ändern. '
    "Bitte vor verbindlicher Kalkulation prüfen. </caption> </table></div>"
)

# Match the GrESt overview table only (after its heading block)
TABLE_RE = re.compile(
    r'(<h2>\s*Grunderwerbsteuer nach Bundesland</h2>\s*'
    r'<p>\s*Übersicht der landesspezifischen.*?</p>\s*)'
    r'<div class="table-responsive">\s*<table\b[^>]*>.*?</table>\s*</div>',
    re.S,
)


def main() -> None:
    text = PATH.read_text(encoding="utf-8", errors="ignore")
    m = TABLE_RE.search(text)
    if not m:
        print("FAIL: GrESt table block not found")
        sys.exit(1)
    updated = TABLE_RE.sub(r"\1" + NEW_TABLE, text, count=1)
    if "Essen und Ruhrgebiet" in updated[m.start() : m.start() + 8000]:
        print("FAIL: standort rows still present near table")
        sys.exit(1)
    if "Baden-Württemberg" not in updated or "Nordrhein-Westfalen" not in updated:
        print("FAIL: expected tax rows missing")
        sys.exit(1)
    PATH.write_text(updated, encoding="utf-8")
    print("OK restored GrESt table with", len(RATES), "rows")


if __name__ == "__main__":
    main()
