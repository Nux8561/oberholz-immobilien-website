#!/usr/bin/env python3
"""Create Bochum-focused Kauf-Landingpages from an existing leistungen template."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "leistungen" / "immobilienverkauf.html"
OUT_DIR = ROOT / "public" / "leistungen"

PAGES = [
    {
        "file": "mehrfamilienhaeuser-kaufen-bochum.html",
        "title": "Mehrfamilienhäuser kaufen in Bochum | Oberholz Immobilien",
        "description": "Mehrfamilienhäuser und Kapitalanlagen in Bochum kaufen – mit lokaler Marktkenntnis von Oberholz Immobilien. Persönliche Beratung vor Ort in Bochum, Zentrale in Münster.",
        "h1": "Mehrfamilienhäuser kaufen in Bochum",
        "lead": "Sie suchen ein Mehrfamilienhaus oder eine renditestarke Kapitalanlage in Bochum? Oberholz Immobilien begleitet Sie persönlich – von der Objektsuche bis zum Notartermin.",
        "nav_label": "Mehrfamilienhäuser kaufen",
    },
    {
        "file": "wohnungen-kaufen-bochum.html",
        "title": "Wohnungen kaufen in Bochum | Oberholz Immobilien",
        "description": "Wohnungen in Bochum kaufen – Eigentumswohnungen und Kapitalanlagen mit lokaler Beratung durch Oberholz Immobilien. Schwerpunkt Bochum, Zentrale in Münster.",
        "h1": "Wohnungen kaufen in Bochum",
        "lead": "Ob Eigennutzung oder Kapitalanlage: Wir finden passende Wohnungen in Bochum und begleiten Sie sicher durch Kauf, Finanzierung und Übergabe.",
        "nav_label": "Wohnungen kaufen",
    },
]


def make_page(spec: dict) -> None:
    html = SRC.read_text(encoding="utf-8", errors="replace")
    html = re.sub(r"<title>[^<]*</title>", f"<title>{spec['title']}</title>", html, count=1)
    html = re.sub(
        r'name="description" content="[^"]*"',
        f'name="description" content="{spec["description"]}"',
        html,
        count=1,
    )
    html = re.sub(
        r'content="[^"]*" name="description"',
        f'content="{spec["description"]}" name="description"',
        html,
        count=1,
    )
    html = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{spec["title"]}"',
        html,
        count=1,
    )
    # Soften sell-focused hero phrases if obvious
    html = html.replace("Immobilienverkauf", spec["nav_label"])
    html = html.replace("Ihre Immobilie verkaufen", spec["h1"])
    html = html.replace("in ganz Deutschland", "in Bochum und Umgebung")
    html = html.replace("Münster, Essen und Bochum", "Bochum und Münster")
    html = html.replace("Münster, Essen, Bochum", "Bochum, Münster")

    # Inject a clear lead paragraph near first container if possible
    inject = (
        f'<div class="container py-4"><div class="row"><div class="col-lg-8">'
        f'<h1 class="h2 mb-3">{spec["h1"]}</h1>'
        f'<p class="lead">{spec["lead"]}</p>'
        f'<p><a class="btn btn-primary" href="/immobilien.html">Aktuelle Objekte ansehen</a> '
        f'<a class="btn btn-outline-secondary ms-2" href="/kontakt/immobilienmakler-bochum.html">Beratung in Bochum</a></p>'
        f"</div></div></div>"
    )
    # Place after <main ...> opening if exists
    html2, n = re.subn(r"(<main\b[^>]*>)", r"\1" + inject, html, count=1, flags=re.I)
    if n:
        html = html2
    else:
        html = html.replace("</header>", "</header>" + inject, 1)

    out = OUT_DIR / spec["file"]
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def add_nav_links() -> None:
    """Add Kauf-links into leistungen dropdown on core pages if missing."""
    link_block = (
        '<li><a href="/leistungen/mehrfamilienhaeuser-kaufen-bochum.html">Mehrfamilienhäuser kaufen</a></li>'
        '<li><a href="/leistungen/wohnungen-kaufen-bochum.html">Wohnungen kaufen</a></li>'
    )
    targets = [ROOT / "index.html"]
    targets += list((ROOT / "public").glob("*.html"))
    targets += list((ROOT / "public" / "leistungen").glob("*.html"))
    changed = 0
    for path in targets:
        html = path.read_text(encoding="utf-8", errors="replace")
        if "mehrfamilienhaeuser-kaufen-bochum.html" in html:
            continue
        # Insert after Immobilienverkauf nav item when present as list item
        new_html, n = re.subn(
            r'(<li>\s*<a href="/leistungen/immobilienverkauf\.html">[^<]*</a>\s*</li>)',
            r"\1" + link_block,
            html,
            count=1,
            flags=re.I,
        )
        if n:
            path.write_text(new_html, encoding="utf-8")
            changed += 1
            print("nav", path.relative_to(ROOT))
    print(f"nav updated on {changed} files")


def main() -> None:
    for spec in PAGES:
        make_page(spec)
    add_nav_links()


if __name__ == "__main__":
    main()
