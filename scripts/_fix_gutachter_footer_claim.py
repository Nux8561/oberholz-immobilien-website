#!/usr/bin/env python3
from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    (
        "sowie zertifizierte Immobiliengutachter",
        "und persönlicher Ansprechpartner vor Ort",
    ),
    (
        "sowie zertifizierte Immobilienmakler",
        "und persönlicher Ansprechpartner vor Ort",
    ),
    (
        "zertifizierte Immobiliengutachter",
        "erfahrene Immobilienmakler",
    ),
]


def main() -> None:
    started = time.time()
    seen = changed = 0
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
        updated = text
        for old, new in REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(
        "DONE",
        {"seen": seen, "changed": changed},
        f"elapsed={time.time()-started:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
