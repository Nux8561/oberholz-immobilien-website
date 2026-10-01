#!/usr/bin/env python3
"""Convert non-Bochum contact city pages to Bochum-first service pages (keep URLs)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KONTAKT = ROOT / "public" / "kontakt"

# keep these cities as real locations
KEEP = {"bochum", "muenster", "essen"}

CITY_SLUG_TO_NAME = {
    "duesseldorf": "Düsseldorf",
    "frankfurt-am-main": "Frankfurt",
    "hamburg": "Hamburg",
    "hannover": "Hannover",
    "muenchen": "München",
    "stuttgart": "Stuttgart",
    "villingen-schwenningen": "Villingen-Schwenningen",
}


def rewrite_file(path: Path, city_name: str) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    html = original

    # Soften nationwide claims
    html = html.replace("in ganz Deutschland", "mit Fokus auf Bochum")
    html = html.replace("ganz Deutschland", "Bochum und Umgebung")
    html = html.replace("deutschlandweit", "in Bochum und Umgebung")

    # Title: keep slug/URL, reframe as Bochum service mentioning the city
    def title_repl(m: re.Match[str]) -> str:
        title = m.group(1)
        if "Bochum" in title and "Oberholz" in title:
            return m.group(0)
        # e.g. Immobilienmakler Hamburg | ...
        return f"<title>Immobilienmakler Bochum – auch für Anfragen aus {city_name} | Oberholz Immobilien</title>"

    html = re.sub(r"<title>([^<]+)</title>", title_repl, html, count=1)

    # Description nudge
    html = re.sub(
        rf'(name="description" content=")([^"]*)(")',
        lambda m: m.group(1)
        + f"Oberholz Immobilien in Bochum: Verkauf, Vermietung und Bewertung. Auch für Eigentümer und Interessenten aus {city_name} – persönlich und lokal."
        + m.group(3),
        html,
        count=1,
    )
    html = re.sub(
        rf'(content=")([^"]*)(" name="description")',
        lambda m: m.group(1)
        + f"Oberholz Immobilien in Bochum: Verkauf, Vermietung und Bewertung. Auch für Eigentümer und Interessenten aus {city_name} – persönlich und lokal."
        + m.group(3),
        html,
        count=1,
    )

    # Visible H1-ish phrases if present
    html = html.replace(f"Immobilienmakler {city_name}", f"Immobilienmakler Bochum (Anfragen aus {city_name})")

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    # top-level kontakt city pages
    for path in KONTAKT.glob("immobilienmakler-*.html"):
        slug = path.stem.replace("immobilienmakler-", "")
        if slug in KEEP:
            continue
        city = CITY_SLUG_TO_NAME.get(slug, slug.replace("-", " ").title())
        if rewrite_file(path, city):
            changed += 1
            print("updated", path.name)

    # nested city topic pages
    for folder in KONTAKT.glob("immobilienmakler-*"):
        if not folder.is_dir():
            continue
        slug = folder.name.replace("immobilienmakler-", "")
        if slug in KEEP:
            continue
        city = CITY_SLUG_TO_NAME.get(slug, slug.replace("-", " ").title())
        for path in folder.glob("*.html"):
            if rewrite_file(path, city):
                changed += 1
                print("updated", path.relative_to(KONTAKT))

    print(f"Done. Changed {changed} kontakt pages.")


if __name__ == "__main__":
    main()
