#!/usr/bin/env python3
"""Replace leftover EE claims in contact-widget with Oberholz facts."""

from __future__ import annotations

from pathlib import Path

PATH = Path("public/theme/contact-widget.html")

REPLACEMENTS = [
    # Badge row (appears in Kontakt + Support sticky footers)
    ("+14.700 Kunden", "Persönlich vor Ort"),
    ("dena und BAFA-zertifiziert", "DIN-zertifizierter Gutachter"),
    ("+20 Jahre Erfahrung", "Bochum &amp; Münster"),
    # Support hotline still EE Stuttgart
    ("0711 – 769 772 24", "0251 28 42 90 90"),
    ("0711 - 769 772 24", "0251 28 42 90 90"),
    ("0711&nbsp;–&nbsp;769&nbsp;772&nbsp;24", "0251&nbsp;28&nbsp;42&nbsp;90&nbsp;90"),
    ("0711&nbsp;-&nbsp;769&nbsp;772&nbsp;24", "0251&nbsp;28&nbsp;42&nbsp;90&nbsp;90"),
    ("tel:+4907117697724", "tel:+4925128429090"),
    ("tel:+4971176977224", "tel:+4925128429090"),
]


def main() -> None:
    html = PATH.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        n = html.count(old)
        if n:
            html = html.replace(old, new)
            print(f"OK {n}x: {old[:50]} -> {new}")
        else:
            print(f"-- miss: {old[:60]}")

    # sanity leftovers
    for bad in ["14.700", "14.000", "dena", "BAFA", "0711", "20 Jahre", "ee-experten"]:
        print("left", bad, html.lower().count(bad.lower()) if bad != "20 Jahre" else html.count(bad))

    PATH.write_text(html, encoding="utf-8")
    print("written", PATH)


if __name__ == "__main__":
    main()
