#!/usr/bin/env python3
"""Finalize Oberholz branding inside restored contact widget."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "public" / "theme" / "contact-widget.html"

REPLACEMENTS = [
    ('src="/media/oberholz-team/michael-oberholz.png "', 'src="/media/oberholz-team/michael-oberholz.png"'),
    ('alt="Peter Holecek"', 'alt="Michael Oberholz"'),
    ('alt="Ute Schorpp"', 'alt="Felix Lesch"'),
    ('alt="Jonas Pischner"', 'alt="Michael Oberholz"'),
    ("Ihre persönlichen Berater", "Ihr Team von Oberholz Immobilien"),
    ("Ihre pers\u00f6nlichen Berater", "Ihr Team von Oberholz Immobilien"),
]


def main() -> None:
    html = PATH.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)

    # Fix any trailing spaces in src attributes
    html = re.sub(r'src="([^"]+?)\s+"', r'src="\1"', html)

    PATH.write_text(html, encoding="utf-8")
    print("updated", PATH)
    print("Michael Oberholz", html.count("Michael Oberholz"))
    print("bad space src", 'michael-oberholz.png "' in html)


if __name__ == "__main__":
    main()
