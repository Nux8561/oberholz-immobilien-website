#!/usr/bin/env python3
"""Bochum-focus audit pass for Oberholz Immobilien static site."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    "node_modules",
    "dist",
    "dist-regionen",
    ".git",
    "analysis",
    "screenshots",
    "reference",
    "immopedia",  # mass encyclopedia; handle separately if needed
}

# Official brand destinations for trust / partner logos
MEDIA_LINKS: dict[str, tuple[str, str]] = {
    # trust / media
    "/media/ard_logo_2019.svg": ("https://www.ard.de/", "ARD"),
    "/media/prosieben_logo.svg": ("https://www.prosieben.de/", "ProSieben"),
    "/media/galileo_logo.svg": ("https://www.galileo.tv/", "Galileo"),
    "/media/logo-rtl.svg": ("https://www.rtl.de/", "RTL"),
    "/media/neues_sat-_1_logo_transparent.png": ("https://www.sat1.de/", "Sat.1"),
    "/media/logo-swr.svg": ("https://www.swr.de/", "SWR"),
    "/media/logo-kabel_1.svg": ("https://www.kabeleins.de/", "Kabel Eins"),
    "/media/logo_antenne_1.svg": ("https://www.antenne1.de/", "Antenne 1"),
    "/media/logo-sz.svg": ("https://www.sueddeutsche.de/", "Süddeutsche Zeitung"),
}

PARTNER_SECTION_NEW = """ <div class="container text-center partner-section"> <h2 class="mb-4">Partner</h2> <div class="d-flex justify-content-center align-items-center flex-wrap partner-logos"> <a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank"> <img alt="DVAG Logo" src="/media/dvag-logo.svg"/> </a> <a href="https://www.swisslife.de/" rel="noopener noreferrer" target="_blank"> <img alt="Swiss Life Logo" src="/media/swiss-life-logo.svg"/> </a> <a href="https://www.interhyp.de/" rel="noopener noreferrer" target="_blank"> <img alt="Interhyp Logo" src="/media/interhyp-logo.svg"/> </a> <a href="https://portal.immobilienscout24.de/ergebnisliste/82828525" rel="noopener noreferrer" target="_blank"> <img alt="ImmoScout24 Logo" src="/media/immoscout.png"/> </a> </div> </div> <style> .partner-logos img { max-height: 50px; margin: 5px 20px; object-fit: contain; } .partner-section { padding: 30px 0; } </style>"""

HEADER_COOP_NEW = (
    ' <div class="col-4"> <span class="extra-small text-muted">In Kooperation mit</span> '
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="DVAG Logo" class="img-fluid w-100" loading="lazy" src="/media/dvag-logo.svg"/>'
    "</a> </div>"
)

FOOTER_COOP_NEW = (
    " <p> In Kooperation mit<br/>"
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="DVAG – Deutsche Vermögensberatung" class="img-fluid" loading="lazy" '
    'src="/media/dvag-logo.svg" style="width: 220px;"/>'
    "</a></p>"
)

# Bochum-first phrasing (Münster remains, Essen softer)
TITLE_REPLACEMENTS = [
    (
        "Immobilienmakler Münster, Essen, Bochum | Oberholz Immobilien",
        "Immobilienmakler Bochum | Oberholz Immobilien – auch Münster",
    ),
]

META_PHRASE_REPLACEMENTS = [
    ("Standorte in Münster, Essen und Bochum.", "Schwerpunkt Bochum – mit Zentrale in Münster."),
    ("Persönlich in Münster, Essen und Bochum.", "Persönlich in Bochum – mit Zentrale in Münster."),
    ("in Münster, Essen und Bochum.", "in Bochum und Münster."),
    ("Münster, Essen und Bochum", "Bochum und Münster"),
    ("Münster, Essen, Bochum", "Bochum, Münster"),
    ("Ihr Immobilienmakler für Münster, Essen und Bochum", "Ihr Immobilienmakler für Bochum"),
    ("für Münster, Essen und Bochum", "für Bochum und Münster"),
    ("in ganz Deutschland", "in Bochum und Umgebung"),
    ("ganz Deutschland", "Bochum und Umgebung"),
    ("deutschlandweit", "in Bochum und Umgebung"),
]


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        # Skip massive regionen bulk for first partner/header pass? Include them for header/footer coop.
        files.append(path)
    return files


def wrap_media_img_with_link(html: str, src: str, url: str, label: str) -> str:
    """Wrap bare <img ... src="SRC" ...> with an anchor if not already linked."""
    # Already wrapped nearby? check pattern <a ...><img ... src=SRC
    already = re.compile(
        rf'<a\b[^>]*>\s*<img\b[^>]*\bsrc="{re.escape(src)}"',
        re.I,
    )
    if already.search(html):
        return html

    pattern = re.compile(
        rf'(<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>)',
        re.I,
    )

    def repl(m: re.Match[str]) -> str:
        img = m.group(1)
        # ensure alt mentions brand if missing
        return (
            f'<a href="{url}" rel="noopener noreferrer" target="_blank" '
            f'title="{label} – offizielle Website">{img}</a>'
        )

    return pattern.sub(repl, html)


def replace_header_coop(html: str) -> str:
    # Header block with Wüstenrot Energieberatung content image
    patterns = [
        re.compile(
            r'<div class="col-4">\s*<span class="extra-small text-muted">In Kooperation mit</span>\s*'
            r'(?:<a[^>]*>\s*)?<img[^>]*(?:Wüstenrot|Wuestenrot|wuestenrot|32697_3_3)[^>]*/?>\s*(?:</a>\s*)?</div>',
            re.I,
        ),
        re.compile(
            r'<div class="col-4">\s*<span class="extra-small text-muted">In Kooperation mit</span>\s*'
            r'(?:<a[^>]*>\s*)?<img[^>]*src="/media/contentimg/32697_3_3\.png"[^>]*/?>\s*(?:</a>\s*)?</div>',
            re.I,
        ),
    ]
    for pat in patterns:
        if pat.search(html):
            return pat.sub(HEADER_COOP_NEW.strip(), html)
    return html


def replace_footer_coop(html: str) -> str:
    patterns = [
        re.compile(
            r"<p>\s*In Kooperation mit<br\s*/?>\s*"
            r'(?:<a[^>]*>\s*)?<img[^>]*src="/media/wuestenrot_bank_201x_logo\.svg"[^>]*/?>\s*(?:</a>\s*)?</p>',
            re.I,
        ),
        re.compile(
            r"<p>\s*In Kooperation mit<br\s*/?>\s*"
            r'(?:<a[^>]*>\s*)?<img[^>]*(?:wuestenrot|Wüstenrot)[^>]*/?>\s*(?:</a>\s*)?</p>',
            re.I,
        ),
    ]
    for pat in patterns:
        if pat.search(html):
            return pat.sub(FOOTER_COOP_NEW.strip(), html)
    return html


def replace_partner_section(html: str) -> str:
    pat = re.compile(
        r'<div class="container text-center partner-section">.*?</style>',
        re.I | re.S,
    )
    if pat.search(html):
        return pat.sub(PARTNER_SECTION_NEW.strip(), html)
    return html


def strip_removed_partner_assets(html: str) -> str:
    # Remove leftover standalone logos if any remain outside partner section
    remove_srcs = [
        "/media/kleinanzeigen.svg",
        "/media/flowfact.png",
        "/media/immowelt.png",
        "/media/wuestenrot_bank_201x_logo.svg",
        "/media/logo_wuestenrot_bausparkasse_ag-optimized.svg",
        "/media/contentimg/32697_3_3.png",
    ]
    for src in remove_srcs:
        # Remove wrapping <a>…</a> that only contains this img
        html = re.sub(
            rf'<a\b[^>]*>\s*<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>\s*</a>',
            "",
            html,
            flags=re.I,
        )
        html = re.sub(
            rf'<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>',
            "",
            html,
            flags=re.I,
        )
    # Text leftovers
    html = html.replace("Wüstenrot Energieberatung", "DVAG")
    html = html.replace("Wuestenrot Energieberatung", "DVAG")
    html = html.replace("Wüstenrot", "DVAG")
    html = html.replace("Wuestenrot", "DVAG")
    return html


def apply_bochum_copy(html: str, path: Path) -> str:
    # Stronger on core pages; lighter on regionen bulk
    is_core = (
        path.name in {"index.html"}
        or path.parent.name in {"public", "leistungen", "ueber-uns", "service", "ratgeber", "kontakt"}
        or path.parent == ROOT
    )
    if not is_core and "regionen" not in path.parts and "immobilien" not in path.parts:
        return html

    for old, new in TITLE_REPLACEMENTS:
        html = html.replace(old, new)

    if is_core or path.name.startswith("immobilienmakler-bochum"):
        for old, new in META_PHRASE_REPLACEMENTS:
            html = html.replace(old, new)
            # case variants already covered mostly
    elif "regionen" in path.parts:
        # Soft: only deutschlandweit claims
        html = html.replace("in ganz Deutschland", "rund um Bochum")
        html = html.replace("ganz Deutschland", "Bochum und Umgebung")
        html = html.replace("deutschlandweit", "in Bochum und Umgebung")
    return html


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    html = original

    html = replace_header_coop(html)
    html = replace_footer_coop(html)
    html = replace_partner_section(html)
    html = strip_removed_partner_assets(html)

    for src, (url, label) in MEDIA_LINKS.items():
        html = wrap_media_img_with_link(html, src, url, label)

    html = apply_bochum_copy(html, path)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    files = iter_html_files()
    changed = 0
    for path in files:
        try:
            if process_file(path):
                changed += 1
                rel = path.relative_to(ROOT)
                print(f"updated: {rel}")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {path}: {exc}", file=sys.stderr)
    print(f"Done. Changed {changed} / {len(files)} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
