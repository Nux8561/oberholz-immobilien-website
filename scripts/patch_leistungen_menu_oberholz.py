#!/usr/bin/env python3
"""Put Oberholz portrait into empty Leistungen mega-menu column; fix München nav img."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBERHOLZ_IMG = "/media/oberholz-team/michael-oberholz.png"

EMPTY_COL = '<div class="col-12 col-md-6"></div>'

FILLED_COL = (
    '<div class="col-12 col-md-6 d-none d-md-flex align-items-end justify-content-center">'
    f'<img alt="Michael Oberholz – Oberholz Immobilien" class="nav-overview-img" '
    f'loading="lazy" src="{OBERHOLZ_IMG}" '
    'style="display:block;width:100%;max-width:280px;height:auto;border-radius:10px;'
    'object-fit:cover;"/>'
    "</div>"
)

# Only replace empty second column that follows the Leistungen vermarktung item
ANCHOR = 'href="/leistungen/immobilienvermarktung.html"'


def patch(html: str) -> str:
    html = html.replace(
        '/media/pillar-card/muenchen.jpg',
        OBERHOLZ_IMG,
    )
    html = html.replace(
        'alt="Kontakt im Überblick"',
        'alt="Michael Oberholz – Oberholz Immobilien"',
    )

    if ANCHOR not in html or EMPTY_COL not in html:
        return html

    # Replace the first empty col that appears after the vermarktung link
    # within a reasonable window (Leistungen mega menu).
    pos = 0
    while True:
        i = html.find(ANCHOR, pos)
        if i < 0:
            break
        window = html[i : i + 600]
        j = window.find(EMPTY_COL)
        if j >= 0:
            abs_j = i + j
            html = html[:abs_j] + FILLED_COL + html[abs_j + len(EMPTY_COL) :]
            pos = abs_j + len(FILLED_COL)
        else:
            pos = i + len(ANCHOR)
    return html


def main() -> None:
    changed = 0
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
        if ANCHOR not in text and "muenchen.jpg" not in text:
            continue
        updated = patch(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print("DONE changed=", changed)


if __name__ == "__main__":
    main()
