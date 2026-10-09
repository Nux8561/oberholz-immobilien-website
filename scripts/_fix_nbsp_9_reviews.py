#!/usr/bin/env python3
"""Fix leftover mobile-menu review count: 9&nbsp;Bewertungen -> 28&nbsp;Bewertungen."""

from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNT = "28"

REPLACEMENTS = [
    (">9&nbsp;Bewertungen<", f">{COUNT}&nbsp;Bewertungen<"),
    ("9&nbsp;Bewertungen", f"{COUNT}&nbsp;Bewertungen"),
    ("9\xa0Bewertungen", f"{COUNT}\xa0Bewertungen"),
]


def main() -> None:
    started = time.time()
    changed = seen = leftovers = 0
    paths = [ROOT / "index.html"]
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)

    for path in paths:
        seen += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "9&nbsp;Bewertungen" not in text and "9\xa0Bewertungen" not in text:
            continue
        updated = text
        for old, new in REPLACEMENTS:
            if old in updated:
                updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
        if "9&nbsp;Bewertungen" in updated or "9\xa0Bewertungen" in updated:
            leftovers += 1
            print("LEFTOVER", path.relative_to(ROOT))

    print(
        f"DONE seen={seen} changed={changed} leftovers={leftovers} "
        f"sec={time.time()-started:.1f}"
    )


if __name__ == "__main__":
    main()
