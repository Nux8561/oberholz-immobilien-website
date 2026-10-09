#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    (
        "sowie <em>zertifizierte Immobilienmakler</em>",
        "und persönlicher Ansprechpartner vor Ort",
    ),
    (
        "sowie <em>zertifizierte Immobiliengutachter</em>",
        "und persönlicher Ansprechpartner vor Ort",
    ),
    (
        "<em>zertifizierte Immobilienmakler</em>",
        "persönlicher Ansprechpartner vor Ort",
    ),
    (
        "<em>zertifizierte Immobiliengutachter</em>",
        "persönlicher Ansprechpartner vor Ort",
    ),
]


def main() -> None:
    changed = 0
    paths = [ROOT / "index.html"]
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        updated = text
        for old, new in REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print("DONE changed=", changed)


if __name__ == "__main__":
    main()
