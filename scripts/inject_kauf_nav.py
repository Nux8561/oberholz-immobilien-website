#!/usr/bin/env python3
"""Inject Kauf-Landingpages into Leistungen dropdown navigation."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_ITEMS = (
    '<a class="dropdown-item" href="/leistungen/mehrfamilienhaeuser-kaufen-bochum.html" '
    'title="Mehrfamilienhäuser kaufen in Bochum"> '
    '<span class="menu-label">Mehrfamilienhäuser kaufen</span></a>'
    '<a class="dropdown-item" href="/leistungen/wohnungen-kaufen-bochum.html" '
    'title="Wohnungen kaufen in Bochum"> '
    '<span class="menu-label">Wohnungen kaufen</span></a>'
)

FOOTERISH = (
    '<a class="" href="/leistungen/mehrfamilienhaeuser-kaufen-bochum.html" '
    'title="Mehrfamilienhäuser kaufen">Mehrfamilienhäuser kaufen'
    '<span class="d-block fw-normal text-muted small">Bochum</span></a>'
    '<a class="" href="/leistungen/wohnungen-kaufen-bochum.html" '
    'title="Wohnungen kaufen">Wohnungen kaufen'
    '<span class="d-block fw-normal text-muted small">Bochum</span></a>'
)


def patch(html: str) -> str:
    if "mehrfamilienhaeuser-kaufen-bochum.html" in html:
        return html

    # Dropdown after Immobilienverkauf
    html2, n = re.subn(
        r'(<a class="dropdown-item" href="/leistungen/immobilienverkauf\.html"[^>]*>.*?</a>)',
        r"\1" + NEW_ITEMS,
        html,
        count=1,
        flags=re.I | re.S,
    )
    if n:
        html = html2

    # Secondary/mobile menu style
    html2, n = re.subn(
        r'(<a class="" href="/leistungen/immobilienverkauf\.html"[^>]*>.*?</a>)',
        r"\1" + FOOTERISH,
        html,
        count=1,
        flags=re.I | re.S,
    )
    if n:
        html = html2
    return html


def main() -> None:
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
    changed = 0
    for path in sorted(set(files)):
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        html = patch(original)
        # Bochum-first meta for leistungen hub
        if path.name == "leistungen.html":
            html = html.replace(
                "Persönlich in Bochum – mit Zentrale in Münster.",
                "Schwerpunkt Bochum – Mehrfamilienhäuser & Wohnungen kaufen, verkaufen und bewerten.",
            )
            if "Mehrfamilienhäuser" not in html.split("<title>", 1)[-1][:80]:
                html = re.sub(
                    r"<title>[^<]*</title>",
                    "<title>Leistungen in Bochum: Kauf, Verkauf, Bewertung | Oberholz Immobilien</title>",
                    html,
                    count=1,
                )
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
