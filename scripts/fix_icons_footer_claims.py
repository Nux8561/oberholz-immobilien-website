#!/usr/bin/env python3
"""Fix LinkedIn icon usage, footer spacing, and legacy inflated claims."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Official LinkedIn brand mark (Simple Icons / brand path)
LINKEDIN_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-label="LinkedIn">'
    "<title>LinkedIn</title>"
    '<path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>'
    "</svg>"
)

FOOTER_WEBSITE = (
    '<span class="h4 text-underline-energy-scale mb-3">Website</span>'
    '<p class="mb-0">'
    '<a href="https://www.platzhirsch-online.de" rel="noopener noreferrer" target="_blank">'
    "Platzhirsch Online Werbeagentur</a><br/>"
    '<span class="extra-small text-muted">Umsetzung &amp; Technik</span>'
    "</p>"
)

# Social block: real icon + clean text
SOCIAL_BLOCK = (
    '<div class="mt-4 d-flex align-items-center gap-2">'
    '<a href="https://www.linkedin.com/company/oberholz-immobilien" '
    'rel="noopener noreferrer" target="_blank" aria-label="Oberholz Immobilien auf LinkedIn" '
    'title="Oberholz Immobilien auf LinkedIn">'
    '<img alt="LinkedIn" height="28" loading="lazy" src="/media/linkedin.svg" '
    'style="width:28px;height:28px;display:block;" width="28"/>'
    "</a>"
    '<a class="text-decoration-none" href="https://www.linkedin.com/company/oberholz-immobilien" '
    'rel="noopener noreferrer" target="_blank">LinkedIn</a>'
    "</div>"
)

CLAIM_REPLACEMENTS = [
    (
        "deutschlandweit verfügbar: Schnelle Terminvergabe, transparente Festpreise, über 11.000 zufriedene Kunden.",
        "Schnelle Terminvergabe, transparente Festpreise, persönliche Beratung vor Ort in Bochum.",
    ),
    (
        "Schnelle Terminvergabe, transparente Festpreise, über 11.000 zufriedene Kunden.",
        "Schnelle Terminvergabe, transparente Festpreise, persönliche Beratung vor Ort in Bochum.",
    ),
    (
        "Schnelle Terminvergabe, transparente Festpreise, &uuml;ber 11.000 zufriedene Kunden.",
        "Schnelle Terminvergabe, transparente Festpreise, persönliche Beratung vor Ort in Bochum.",
    ),
    (
        "über 11.000 zufriedene Kunden",
        "persönliche Beratung vor Ort in Bochum",
    ),
    (
        "&uuml;ber 11.000 zufriedene Kunden",
        "persönliche Beratung vor Ort in Bochum",
    ),
    (
        "+14.700 zufriedene Kunden",
        "Persönliche Beratung in Bochum",
    ),
    (
        "+14.700 zufriedene Kunden ",
        "Persönliche Beratung in Bochum ",
    ),
    (
        "Unsere Kunden profitieren von einem <strong>bundesweiten Netzwerk</strong>, einer <strong>hauseigenen Werbeagentur</strong>",
        "Unsere Kunden profitieren von <strong>lokaler Marktkenntnis in Bochum</strong> und einer <strong>klaren Vermarktungsstrategie</strong>",
    ),
    (
        "mit über zwei Jahrzehnten Erfahrung in der Immobilienvermarktung sowie von unserem Sta",
        "mit fundierter Erfahrung in der Immobilienvermarktung sowie von unserem Sta",
    ),
    (
        "Führende Immobilienportale, Suchkunden und Partnernetzwerk.",
        "Führende Immobilienportale und persönliche Betreuung vor Ort.",
    ),
    (
        "eine eigeneWerbeagentur mit über 20 Jahren Erfahrung",
        "starke Vermarktung mit lokalem Fokus auf Bochum",
    ),
    (
        "eine eigene <em>Werbeagentur mit über 20 Jahren Erfahrung</em>",
        "starke <em>Vermarktung mit lokalem Fokus auf Bochum</em>",
    ),
    (
        "über 20 Jahre Erfahrung in Immobilienmarketing &amp; Unternehmenskommunikation",
        "fundierte Erfahrung in Immobilienvermarktung und Kundenberatung",
    ),
    (
        "Die <strong>Oberholz Immobilien</strong> stehen seit über 20 Jahren für gebündelte Fachkompetenz",
        "Die <strong>Oberholz Immobilien</strong> stehen für gebündelte Fachkompetenz",
    ),
]

# Remove EE brochure external link → local media if present
EE_LINK_PAT = re.compile(
    r'href="https://www\.ee-experten\.de/media/([^"]+)"',
    re.I,
)


def replace_footer_website(html: str) -> str:
    html = re.sub(
        r'<span class="h4 text-underline-energy-scale mb-3">Website</span>'
        r'(?:<p[^>]*>.*?</p>)+',
        FOOTER_WEBSITE,
        html,
        flags=re.I | re.S,
    )
    return html


def replace_social(html: str) -> str:
    # Old flex block with linkedin image + paragraph
    html = re.sub(
        r'<div class="mt-5"[^>]*>\s*'
        r'<a href="https://www\.linkedin\.com/company/oberholz-immobilien"[^>]*>\s*'
        r'<img[^>]*linkedin\.svg[^>]*/?>\s*</a>\s*'
        r"<p[^>]*>.*?</p>\s*</div>",
        SOCIAL_BLOCK,
        html,
        flags=re.I | re.S,
    )
    # Also catch slightly different attribute order / mt-5 class position
    html = re.sub(
        r'<div[^>]*class="mt-5"[^>]*style="display:\s*flex[^"]*"[^>]*>\s*'
        r'<a href="https://www\.linkedin\.com/company/oberholz-immobilien"[^>]*>.*?</a>\s*'
        r"<p[^>]*>.*?linkedin\.com/company/oberholz-immobilien.*?</p>\s*</div>",
        SOCIAL_BLOCK,
        html,
        flags=re.I | re.S,
    )
    return html


def process(html: str) -> str:
    html = replace_footer_website(html)
    html = replace_social(html)
    for old, new in CLAIM_REPLACEMENTS:
        html = html.replace(old, new)
    # local brochure fallback
    html = EE_LINK_PAT.sub(r'href="/media/\1"', html)
    return html


def collect() -> list[Path]:
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
        if folder.name == "kontakt":
            files.extend(folder.glob("*/*.html"))
    files.extend((ROOT / "public" / "immobilien").rglob("*.html"))
    return sorted({p for p in files if p.is_file()})


def main() -> None:
    (ROOT / "public" / "media" / "linkedin.svg").write_text(LINKEDIN_SVG, encoding="utf-8")
    print("linkedin.svg written")

    changed = 0
    for path in collect():
        original = path.read_text(encoding="utf-8", errors="replace")
        html = process(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
