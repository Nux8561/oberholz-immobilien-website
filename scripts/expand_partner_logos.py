#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

FOOTER_PARTNERS = (
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

HEADER_PARTNERS = (
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


def patch(html: str) -> str:
    html = re.sub(
        r'<div class="col-4">\s*<span class="extra-small text-muted">In Kooperation mit</span>.*?</div>',
        HEADER_PARTNERS,
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = re.sub(
        r"<p>\s*In Kooperation mit<br\s*/?>.*?</p>",
        FOOTER_PARTNERS,
        html,
        count=1,
        flags=re.I | re.S,
    )
    return html


def main() -> None:
    files = [ROOT / "index.html"]
    files += list((ROOT / "public").glob("*.html"))
    files += list((ROOT / "public" / "leistungen").glob("*.html"))
    files += list((ROOT / "public" / "ueber-uns").glob("*.html"))
    files += list((ROOT / "public" / "service").glob("*.html"))
    files += list((ROOT / "public" / "kontakt").glob("*.html"))
    changed = 0
    for path in sorted(set(files)):
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        html = patch(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
