#!/usr/bin/env python3
"""Put Essen first in the DIN topbar claim across all HTML."""

from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    (
        "DIN-zertifizierter Immobilienmakler | Münster · Essen · Bochum",
        "Immobilienmakler in Essen | auch Münster · Bochum",
    ),
    (
        "DIN-zertifizierter Immobilienmakler | Bochum · Münster · Essen",
        "Immobilienmakler in Essen | auch Münster · Bochum",
    ),
    (
        "Standorte Bochum, Münster und Essen",
        "Schwerpunkt Essen – auch Münster und Bochum",
    ),
    (
        "DIN-zertifizierter Immobilienmakler Michael Oberholz ermittelt belastbare Marktwerte",
        "Das Team von Oberholz Immobilien ermittelt belastbare Marktwerte",
    ),
    (
        "Deutschlandweit einmalig",
        "Persönlich vor Ort",
    ),
]


def iter_html():
    yield ROOT / "index.html"
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                yield Path(dirpath) / name


def main() -> None:
    started = time.time()
    seen = changed = 0
    for path in iter_html():
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
        if seen % 2000 == 0:
            print(f"progress {seen} changed={changed}", flush=True)
    print(
        "DONE",
        {"seen": seen, "changed": changed},
        f"elapsed={time.time()-started:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
