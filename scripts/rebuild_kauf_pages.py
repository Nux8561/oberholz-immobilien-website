#!/usr/bin/env python3
"""Rebuild Kauf-Landingpages cleanly from immobilienverkauf template."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "leistungen" / "immobilienverkauf.html"

# Use index nav as canonical (has Kauf links already)
INDEX = ROOT / "index.html"

PAGES = [
    {
        "file": "mehrfamilienhaeuser-kaufen-bochum.html",
        "title": "Mehrfamilienhäuser kaufen in Bochum | Oberholz Immobilien",
        "description": "Mehrfamilienhäuser und Kapitalanlagen in Bochum kaufen – mit lokaler Marktkenntnis von Oberholz Immobilien. Persönliche Beratung vor Ort in Bochum, Zentrale in Münster.",
        "h1": "Mehrfamilienhäuser kaufen in Bochum",
        "lead": "Sie suchen ein Mehrfamilienhaus oder eine renditestarke Kapitalanlage in Bochum? Oberholz Immobilien begleitet Sie persönlich – von der Objektsuche bis zum Notartermin.",
    },
    {
        "file": "wohnungen-kaufen-bochum.html",
        "title": "Wohnungen kaufen in Bochum | Oberholz Immobilien",
        "description": "Wohnungen in Bochum kaufen – Eigentumswohnungen und Kapitalanlagen mit lokaler Beratung durch Oberholz Immobilien. Schwerpunkt Bochum, Zentrale in Münster.",
        "h1": "Wohnungen kaufen in Bochum",
        "lead": "Ob Eigennutzung oder Kapitalanlage: Wir finden passende Wohnungen in Bochum und begleiten Sie sicher durch Kauf, Finanzierung und Übergabe.",
    },
]


def extract_nav(html: str) -> str | None:
    m = re.search(r"(<nav\b[^>]*>.*?</nav>)", html, re.I | re.S)
    return m.group(1) if m else None


def main() -> None:
    base = SRC.read_text(encoding="utf-8", errors="replace")
    index_html = INDEX.read_text(encoding="utf-8", errors="replace")
    index_nav = extract_nav(index_html)
    if not index_nav:
        raise SystemExit("No nav found in index.html")

    for spec in PAGES:
        html = base
        # Replace ALL nav blocks with canonical index nav
        html = re.sub(r"<nav\b[^>]*>.*?</nav>", index_nav, html, count=1, flags=re.I | re.S)

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

        inject = (
            f'<div class="container py-4"><div class="row"><div class="col-lg-8">'
            f'<p class="text-muted mb-2">Oberholz Immobilien · Bochum</p>'
            f'<h1 class="h2 mb-3">{spec["h1"]}</h1>'
            f'<p class="lead">{spec["lead"]}</p>'
            f'<p><a class="btn btn-primary" href="/immobilien.html">Aktuelle Objekte ansehen</a> '
            f'<a class="btn btn-outline-secondary ms-2" href="/kontakt/immobilienmakler-bochum.html">Beratung in Bochum</a> '
            f'<a class="btn btn-outline-secondary ms-2" href="/service/kann-ich-kaufen.html">Budget prüfen</a></p>'
            f"</div></div></div>"
        )
        # Remove previous inject if regenerating
        html = re.sub(
            r'<div class="container py-4"><div class="row"><div class="col-lg-8">.*?</div></div></div>',
            "",
            html,
            count=1,
            flags=re.S,
        )
        html2, n = re.subn(r"(<main\b[^>]*>)", r"\1" + inject, html, count=1, flags=re.I)
        html = html2 if n else html.replace("</header>", "</header>" + inject, 1)

        out = ROOT / "public" / "leistungen" / spec["file"]
        out.write_text(html, encoding="utf-8")
        print("rewrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
