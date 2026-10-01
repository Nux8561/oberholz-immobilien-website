#!/usr/bin/env python3
"""Reorder Standort-Nav: Bochum first, then Münster, then Essen."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Common repeated nav fragment patterns (order Münster, Essen, Bochum)
PATTERNS = [
    # link order without labels between
    (
        re.compile(
            r'(href="/kontakt/immobilienmakler-muenster\.html"[^>]*>)(.*?)(</a>)'
            r'(.*?)'
            r'(href="/kontakt/immobilienmakler-essen\.html"[^>]*>)(.*?)(</a>)'
            r'(.*?)'
            r'(href="/kontakt/immobilienmakler-bochum\.html"[^>]*>)(.*?)(</a>)',
            re.S,
        ),
        r'\9\10\11\8\1\2\3\4\5\6\7',  # bochum, muenster, essen — may be fragile
    ),
]


def reorder_simple(html: str) -> str:
    """Swap sequential Münster→Essen→Bochum link triples into Bochum→Münster→Essen."""
    # Work on compact triples of li items if present
    li_pat = re.compile(
        r'(<li[^>]*>\s*<a[^>]+href="/kontakt/immobilienmakler-muenster\.html"[^>]*>.*?</a>\s*</li>\s*)'
        r'(<li[^>]*>\s*<a[^>]+href="/kontakt/immobilienmakler-essen\.html"[^>]*>.*?</a>\s*</li>\s*)'
        r'(<li[^>]*>\s*<a[^>]+href="/kontakt/immobilienmakler-bochum\.html"[^>]*>.*?</a>\s*</li>)',
        re.I | re.S,
    )
    html = li_pat.sub(r"\3\1\2", html)

    # Also handle bare consecutive anchors in some menus
    a_pat = re.compile(
        r'(<a[^>]+href="/kontakt/immobilienmakler-muenster\.html"[^>]*>.*?</a>\s*)'
        r'(<a[^>]+href="/kontakt/immobilienmakler-essen\.html"[^>]*>.*?</a>\s*)'
        r'(<a[^>]+href="/kontakt/immobilienmakler-bochum\.html"[^>]*>.*?</a>)',
        re.I | re.S,
    )
    html = a_pat.sub(r"\3\1\2", html)
    return html


def main() -> None:
    files = [ROOT / "index.html"]
    files += list((ROOT / "public").glob("*.html"))
    files += list((ROOT / "public" / "leistungen").glob("*.html"))
    files += list((ROOT / "public" / "ueber-uns").glob("*.html"))
    files += list((ROOT / "public" / "service").glob("*.html"))
    files += list((ROOT / "public" / "ratgeber").glob("*.html"))
    files += list((ROOT / "public" / "kontakt").glob("*.html"))
    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8", errors="replace")
        html = reorder_simple(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
