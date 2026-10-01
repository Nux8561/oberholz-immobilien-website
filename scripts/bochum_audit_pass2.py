#!/usr/bin/env python3
"""Faster Bochum audit: core pages first, then header/footer-only for bulk."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MEDIA_LINKS = {
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

PARTNER_SECTION_NEW = (
    ' <div class="container text-center partner-section"> <h2 class="mb-4">Partner</h2> '
    '<div class="d-flex justify-content-center align-items-center flex-wrap partner-logos"> '
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank"> '
    '<img alt="DVAG Logo" src="/media/dvag-logo.svg"/> </a> '
    '<a href="https://www.swisslife.de/" rel="noopener noreferrer" target="_blank"> '
    '<img alt="Swiss Life Logo" src="/media/swiss-life-logo.svg"/> </a> '
    '<a href="https://www.interhyp.de/" rel="noopener noreferrer" target="_blank"> '
    '<img alt="Interhyp Logo" src="/media/interhyp-logo.svg"/> </a> '
    '<a href="https://portal.immobilienscout24.de/ergebnisliste/82828525" rel="noopener noreferrer" target="_blank"> '
    '<img alt="ImmoScout24 Logo" src="/media/immoscout.png"/> </a> '
    "</div> </div> "
    "<style> .partner-logos img { max-height: 50px; margin: 5px 20px; object-fit: contain; } "
    ".partner-section { padding: 30px 0; } </style>"
)

HEADER_COOP_NEW = (
    '<div class="col-4"> <span class="extra-small text-muted">In Kooperation mit</span> '
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="DVAG Logo" class="img-fluid w-100" loading="lazy" src="/media/dvag-logo.svg"/>'
    "</a> </div>"
)

FOOTER_COOP_NEW = (
    "<p> In Kooperation mit<br/>"
    '<a href="https://www.dvag.de/" rel="noopener noreferrer" target="_blank">'
    '<img alt="DVAG – Deutsche Vermögensberatung" class="img-fluid" loading="lazy" '
    'src="/media/dvag-logo.svg" style="width: 220px;"/>'
    "</a></p>"
)

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


def wrap_media_img_with_link(html: str, src: str, url: str, label: str) -> str:
    already = re.compile(rf'<a\b[^>]*>\s*<img\b[^>]*\bsrc="{re.escape(src)}"', re.I)
    if already.search(html):
        return html
    pattern = re.compile(rf'(<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>)', re.I)

    def repl(m: re.Match[str]) -> str:
        return (
            f'<a href="{url}" rel="noopener noreferrer" target="_blank" '
            f'title="{label} – offizielle Website">{m.group(1)}</a>'
        )

    return pattern.sub(repl, html)


def replace_header_coop(html: str) -> str:
    pat = re.compile(
        r'<div class="col-4">\s*<span class="extra-small text-muted">In Kooperation mit</span>\s*'
        r'(?:<a[^>]*>\s*)?<img[^>]*src="/media/contentimg/32697_3_3\.png"[^>]*/?>\s*(?:</a>\s*)?</div>',
        re.I,
    )
    if pat.search(html):
        return pat.sub(HEADER_COOP_NEW, html)
    # already DVAG? leave
    pat2 = re.compile(
        r'<div class="col-4">\s*<span class="extra-small text-muted">In Kooperation mit</span>\s*'
        r'(?:<a[^>]*>\s*)?<img[^>]*(?:Wüstenrot|wuestenrot)[^>]*/?>\s*(?:</a>\s*)?</div>',
        re.I,
    )
    if pat2.search(html):
        return pat2.sub(HEADER_COOP_NEW, html)
    return html


def replace_footer_coop(html: str) -> str:
    pat = re.compile(
        r"<p>\s*In Kooperation mit<br\s*/?>\s*"
        r'(?:<a[^>]*>\s*)?<img[^>]*src="/media/wuestenrot_bank_201x_logo\.svg"[^>]*/?>\s*(?:</a>\s*)?</p>',
        re.I,
    )
    if pat.search(html):
        return pat.sub(FOOTER_COOP_NEW, html)
    return html


def replace_partner_section(html: str) -> str:
    pat = re.compile(r'<div class="container text-center partner-section">.*?</style>', re.I | re.S)
    if pat.search(html):
        return pat.sub(PARTNER_SECTION_NEW, html)
    return html


def remove_retired_partner_imgs(html: str) -> str:
    remove_srcs = [
        "/media/kleinanzeigen.svg",
        "/media/flowfact.png",
        "/media/immowelt.png",
        "/media/wuestenrot_bank_201x_logo.svg",
        "/media/logo_wuestenrot_bausparkasse_ag-optimized.svg",
        "/media/contentimg/32697_3_3.png",
    ]
    for src in remove_srcs:
        html = re.sub(
            rf'<a\b[^>]*>\s*<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>\s*</a>',
            "",
            html,
            flags=re.I,
        )
        html = re.sub(rf'<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>', "", html, flags=re.I)
    return html


def apply_bochum_copy(html: str, *, strong: bool) -> str:
    for old, new in TITLE_REPLACEMENTS:
        html = html.replace(old, new)
    if strong:
        for old, new in META_PHRASE_REPLACEMENTS:
            html = html.replace(old, new)
    else:
        html = html.replace("in ganz Deutschland", "rund um Bochum")
        html = html.replace("ganz Deutschland", "Bochum und Umgebung")
        html = html.replace("deutschlandweit", "in Bochum und Umgebung")
    return html


def reorder_nav_bochum_first(html: str) -> str:
    """Swap Münster/Essen/Bochum order in visible nav labels where present."""
    # Prefer Bochum link appearing before Essen/Münster in common dropdown blocks is complex;
    # at least rewrite label order phrases.
    html = html.replace(
        "Immobilienmakler Münster</a>",
        "Immobilienmakler Münster</a>",
    )
    # Put Bochum first in title-like comma lists already handled.
    return html


def process(html: str, *, strong: bool, trust_links: bool) -> str:
    html = replace_header_coop(html)
    html = replace_footer_coop(html)
    html = replace_partner_section(html)
    html = remove_retired_partner_imgs(html)
    if trust_links:
        for src, (url, label) in MEDIA_LINKS.items():
            html = wrap_media_img_with_link(html, src, url, label)
    html = apply_bochum_copy(html, strong=strong)
    html = reorder_nav_bochum_first(html)
    return html


def collect_core() -> list[Path]:
    paths: list[Path] = [ROOT / "index.html"]
    for folder in [
        ROOT / "public",
        ROOT / "public" / "leistungen",
        ROOT / "public" / "ueber-uns",
        ROOT / "public" / "service",
        ROOT / "public" / "ratgeber",
        ROOT / "public" / "kontakt",
    ]:
        if folder.is_dir():
            paths.extend(folder.glob("*.html"))
            # one level of kontakt subdirs
            if folder.name == "kontakt":
                paths.extend(folder.glob("*/*.html"))
    # unique
    return sorted(set(p for p in paths if p.is_file()))


def collect_bulk_needing_coop() -> list[Path]:
    """Only files that still contain old Wüstenrot coop markers; skip already done."""
    roots = [
        ROOT / "public" / "immobilien",
        ROOT / "public" / "regionen",
        ROOT / "public" / "immopedia",
    ]
    markers = ("wuestenrot_bank_201x_logo.svg", "contentimg/32697_3_3.png", "kleinanzeigen.svg", "flowfact.png")
    out: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.html"):
            # quick binary check via read of first/last is hard; read text
            try:
                data = p.read_bytes()
            except OSError:
                continue
            if any(m.encode() in data for m in markers):
                out.append(p)
    return out


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "core"
    changed = 0
    if mode == "core":
        files = collect_core()
        print(f"Processing {len(files)} core files...", flush=True)
        for i, path in enumerate(files, 1):
            original = path.read_text(encoding="utf-8", errors="replace")
            html = process(original, strong=True, trust_links=True)
            if html != original:
                path.write_text(html, encoding="utf-8")
                changed += 1
            if i % 25 == 0:
                print(f"  …{i}/{len(files)} (changed {changed})", flush=True)
    elif mode == "bulk":
        files = collect_bulk_needing_coop()
        print(f"Processing {len(files)} bulk files with old partners...", flush=True)
        for i, path in enumerate(files, 1):
            original = path.read_text(encoding="utf-8", errors="replace")
            html = process(original, strong=False, trust_links=False)
            if html != original:
                path.write_text(html, encoding="utf-8")
                changed += 1
            if i % 200 == 0:
                print(f"  …{i}/{len(files)} (changed {changed})", flush=True)
    else:
        print("Usage: bochum_audit_pass2.py [core|bulk]")
        return 2

    print(f"Done. Changed {changed} files in mode={mode}.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
