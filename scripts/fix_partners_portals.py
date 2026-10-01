#!/usr/bin/env python3
"""Restore portals + add DVAG/Swiss Life/Interhyp; keep Flowfact out."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PARTNER_SECTION = """ <div class="container text-center partner-section"> <h2 class="mb-4">Partner</h2> <div class="d-flex justify-content-center align-items-center flex-wrap partner-logos"> <a href="https://www.kleinanzeigen.de/" rel="noopener noreferrer" target="_blank"> <img alt="eBay Kleinanzeigen Logo" src="/media/kleinanzeigen.svg"/> </a> <a href="https://www.immowelt.de/" rel="noopener noreferrer" target="_blank"> <img alt="Immowelt Logo" src="/media/immowelt.png"/> </a> <a href="https://portal.immobilienscout24.de/ergebnisliste/82828525" rel="noopener noreferrer" target="_blank"> <img alt="ImmoScout24 Logo" src="/media/immoscout.png"/> </a> <a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank"> <img alt="DVAG Logo" src="/media/dvag-logo.svg"/> </a> <a href="https://www.swisslife.de/" rel="noopener noreferrer" target="_blank"> <img alt="Swiss Life Logo" src="/media/swiss-life-logo.svg"/> </a> <a href="https://www.interhyp.de/" rel="noopener noreferrer" target="_blank"> <img alt="Interhyp Logo" src="/media/interhyp-logo.svg"/> </a> </div> </div> <style> .partner-logos img { max-height: 50px; margin: 5px 20px; object-fit: contain; } .partner-section { padding: 30px 0; } </style>"""

HEADER_COOP = (
    '<div class="col-4"> <span class="extra-small text-muted">In Kooperation mit</span> '
    '<div class="d-flex align-items-center gap-2 flex-wrap">'
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="DVAG Logo" class="img-fluid" loading="lazy" src="/media/dvag-logo.svg" style="max-height:42px;"/></a>'
    '<a href="https://www.swisslife.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="Swiss Life Logo" class="img-fluid" loading="lazy" src="/media/swiss-life-logo.svg" style="max-height:36px;"/></a>'
    '<a href="https://www.interhyp.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="Interhyp Logo" class="img-fluid" loading="lazy" src="/media/interhyp-logo.svg" style="max-height:36px;"/></a>'
    "</div></div>"
)

FOOTER_COOP = (
    "<p> In Kooperation mit<br/>"
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="DVAG – Deutsche Vermögensberatung" class="img-fluid" loading="lazy" '
    'src="/media/dvag-logo.svg" style="width: 180px; margin-right: 12px;"/></a> '
    '<a href="https://www.swisslife.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="Swiss Life" class="img-fluid" loading="lazy" '
    'src="/media/swiss-life-logo.svg" style="width: 140px; margin-right: 12px;"/></a> '
    '<a href="https://www.interhyp.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="Interhyp" class="img-fluid" loading="lazy" '
    'src="/media/interhyp-logo.svg" style="width: 140px;"/></a></p>'
)


def process(html: str) -> str:
    # Restore/replace partner strip wherever present
    if "partner-section" in html:
        html = re.sub(
            r'<div class="container text-center partner-section">.*?</style>',
            PARTNER_SECTION.strip(),
            html,
            count=1,
            flags=re.I | re.S,
        )
    # Header coop
    html = re.sub(
        r'<div class="col-4">\s*<span class="extra-small text-muted">In Kooperation mit</span>.*?</div>',
        HEADER_COOP,
        html,
        count=1,
        flags=re.I | re.S,
    )
    # Footer coop
    html = re.sub(
        r"<p>\s*In Kooperation mit<br\s*/?>.*?</p>",
        FOOTER_COOP,
        html,
        count=1,
        flags=re.I | re.S,
    )
    # Ensure Flowfact stays gone if somehow reintroduced
    html = re.sub(
        r'<a\b[^>]*>\s*<img\b[^>]*\bsrc="/media/flowfact\.png"[^>]*/?>\s*</a>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r'<img\b[^>]*\bsrc="/media/flowfact\.png"[^>]*/?>', "", html, flags=re.I)
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
        html = process(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
