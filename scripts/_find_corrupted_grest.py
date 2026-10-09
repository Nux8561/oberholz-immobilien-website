# -*- coding: utf-8 -*-
"""Find tables whose headers say Bundesland/Steuersatz but body has standort rows."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]

TABLE_RE = re.compile(r"<table\b[^>]*>.*?</table>", re.S | re.I)


def main() -> None:
    hits = []
    paths = [ROOT / "index.html"]
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)

    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "Steuersatz" not in text and "Grunderwerbsteuer" not in text:
            continue
        for m in TABLE_RE.finditer(text):
            tbl = m.group(0)
            has_header = "Steuersatz" in tbl or (
                "Bundesland" in tbl and "thead" in tbl.lower()
            )
            has_standort = "Essen und Ruhrgebiet" in tbl or "Münster und Münsterland" in tbl
            has_tax_row = "Baden-Württemberg" in tbl and "%" in tbl
            if has_standort and ("Steuersatz" in tbl or "Bundesland" in tbl[:800]):
                hits.append((str(path.relative_to(ROOT)), "standort-in-tax", len(tbl)))
            elif "Steuersatz" in tbl and not has_tax_row and "Vor Ort" in tbl:
                hits.append((str(path.relative_to(ROOT)), "vor-ort-in-tax", len(tbl)))

    print(f"hits={len(hits)}")
    for h in hits:
        print(h)


if __name__ == "__main__":
    main()
