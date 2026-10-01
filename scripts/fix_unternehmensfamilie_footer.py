#!/usr/bin/env python3
"""Replace fake Unternehmens-Familie footer with Platzhirsch agency credit."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_BLOCK = (
    '<span class="h4 text-underline-energy-scale mb-3">Website</span>'
    '<p class="mb-1">Umsetzung &amp; Technik</p>'
    '<p><a href="https://www.platzhirsch-online.de" rel="noopener noreferrer" target="_blank">'
    "&raquo; Platzhirsch Online Werbeagentur</a></p>"
)

# Match heading + following family links until next column/widget
PATTERN = re.compile(
    r'<span class="h4 text-underline-energy-scale mb-3">Unternehmens-Familie</span>'
    r"(?:(?!</div>\s*</div>\s*<div class=\"d-block).)*?"
    r"(?=</div>\s*</div>\s*<div class=\"d-block)",
    re.I | re.S,
)

# Broader fallback: heading through last family <p>...</p> before closing widget divs
PATTERN2 = re.compile(
    r'<span class="h4 text-underline-energy-scale mb-3">Unternehmens-Familie</span>'
    r"(?:\s*<p>.*?</p>)+",
    re.I | re.S,
)


def process(html: str) -> str:
    html2, n = PATTERN.subn(NEW_BLOCK, html)
    if n:
        return html2
    html2, n = PATTERN2.subn(NEW_BLOCK, html)
    return html2


def collect() -> list[Path]:
    files = [ROOT / "index.html"]
    for folder in [
        ROOT / "public",
        ROOT / "public" / "leistungen",
        ROOT / "public" / "ueber-uns",
        ROOT / "public" / "service",
        ROOT / "public" / "ratgeber",
        ROOT / "public" / "kontakt",
    ]:
        files.extend(folder.glob("*.html"))
        if folder.name == "kontakt":
            files.extend(folder.glob("*/*.html"))
    # exposés also often share footer
    files.extend((ROOT / "public" / "immobilien").rglob("*.html"))
    return sorted({p for p in files if p.is_file()})


def main() -> None:
    changed = 0
    for path in collect():
        original = path.read_text(encoding="utf-8", errors="replace")
        if "Unternehmens-Familie" not in original:
            continue
        html = process(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
        else:
            print("UNCHANGED", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
