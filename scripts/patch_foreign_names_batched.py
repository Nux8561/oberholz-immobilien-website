"""Patch old person names in priority HTML sets, then regionen in chunks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = (
    ("Kersten Streit", "Michael Oberholz"),
    ("Wolfgang Mayer", "Felix Lesch"),
    ("Axel Winkler", "Michael Penn"),
    ("René Mohr", "Pascal Kopp"),
    ("Rene Mohr", "Pascal Kopp"),
    ("Ren&eacute; Mohr", "Pascal Kopp"),
    ("Christian Munz", "Lubka Röger"),
    ("Gebietsleiterin Immobilienverkauf", "Immobilienberaterin"),
    ("Gebietsleiter Immobilienverkauf", "Immobilienberater"),
    ("Leitung Immobilienverkauf", "Inhaber &amp; Sachverständiger"),
    ("Leitung Immobilienvermittlung", "Inhaber &amp; Sachverständiger"),
    ("Leiter Immobilienverkauf", "Inhaber &amp; Sachverständiger"),
    ("streit_facepile.jpg", "oberholz_facepile.jpg"),
)


def patch_file(path: Path) -> int:
    try:
        data = path.read_bytes()
    except OSError:
        return 0
    # Detect encoding lightly
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("utf-8", "replace")
    original = text
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
    text = text.replace(
        "Lubka Röger - Immobilienberater",
        "Lubka Röger - Immobilienberaterin",
    )
    if text == original:
        return 0
    path.write_text(text, encoding="utf-8")
    return 1


def collect(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_file() and p.suffix.lower() == ".html":
            out.append(p)
        elif p.is_dir():
            out.extend(p.rglob("*.html"))
    return out


def main() -> None:
    priority = [
        ROOT / "index.html",
        *sorted((ROOT / "public").glob("*.html")),
        ROOT / "public" / "immobilien",
        ROOT / "public" / "immopedia",
        ROOT / "public" / "whitepaper-wohnwechsel-im-alter.html",
    ]
    # extra whitepapers already covered by public/*.html

    files = collect(priority)
    print("priority files", len(files))
    changed = sum(patch_file(p) for p in files)
    print("priority changed", changed)

    regionen = ROOT / "public" / "regionen"
    if regionen.exists():
        # Process alphabetically in batches with progress
        cities = sorted([d for d in regionen.iterdir() if d.is_dir()])
        total_c = 0
        total_f = 0
        for i, city in enumerate(cities, 1):
            city_files = list(city.rglob("*.html"))
            c = sum(patch_file(p) for p in city_files)
            total_c += c
            total_f += len(city_files)
            if i % 200 == 0 or i == len(cities):
                print(f"regionen {i}/{len(cities)} cities, files {total_f}, changed {total_c}")
        print("regionen done", "files", total_f, "changed", total_c)


if __name__ == "__main__":
    main()
