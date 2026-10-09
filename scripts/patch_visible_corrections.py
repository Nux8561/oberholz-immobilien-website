#!/usr/bin/env python3
"""Visible corrections: remove rainbow claims leftovers in HTML, media/ImmoScout,
energy/gutachten services, and reframe chrome copy to Essen-first.
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MEDIA_SRCS = [
    "/media/ard_logo_2019.svg",
    "/media/prosieben_logo.svg",
    "/media/galileo_logo.svg",
    "/media/logo-rtl.svg",
    "/media/neues_sat-_1_logo_transparent.png",
    "/media/logo-swr.svg",
    "/media/logo-kabel_1.svg",
    "/media/logo_antenne_1.svg",
    "/media/logo-sz.svg",
    "/media/immoscout.png",
]

SERVICE_PATHS = [
    "/leistungen/immobilienbewertung.html",
    "/leistungen/energieberatung.html",
    "/leistungen/energieausweis-kostenlos.html",
]

RETIRED_PAGES = [
    ROOT / "public" / "leistungen" / "immobilienbewertung.html",
    ROOT / "public" / "leistungen" / "energieberatung.html",
    ROOT / "public" / "leistungen" / "energieausweis-kostenlos.html",
]

FOOTER_OLD = (
    "Die <strong>Oberholz Immobilien</strong> verbinden Immobilienvermittlung mit "
    "einzigartiger Energiekompetenz. Wir ermitteln den realistischen Marktwert, "
    "bereiten alle Unterlagen von Grundrissen bis Energieausweisen professionell auf "
    "und begleiten Sie persönlich – von der ersten Bewertung bis zum erfolgreichen "
    "Vertragsabschluss, in Bochum und Umgebung."
)

FOOTER_OLD_ALT = (
    "Die <strong>Oberholz Immobilien</strong> verbinden Immobilienvermittlung mit "
    "fundierter Markt- und Gutachterkompetenz. Wir ermitteln den realistischen Marktwert, "
    "bereiten alle Unterlagen von Grundrissen bis Energieausweisen professionell auf "
    "und begleiten Sie persönlich – von der ersten Bewertung bis zum erfolgreichen "
    "Vertragsabschluss, in Bochum und Münster."
)

FOOTER_NEW = (
    "Die <strong>Oberholz Immobilien</strong> stehen für persönliche Immobilienvermittlung "
    "in Essen und Umgebung. Wir begleiten Verkauf und Vermietung transparent – von der "
    "ersten Einschätzung bis zum erfolgreichen Vertragsabschluss."
)

STUB_HTML = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex, follow"/>
<link rel="canonical" href="/leistungen.html"/>
<title>Leistung nicht verfügbar | Oberholz Immobilien</title>
<meta name="description" content="Diese Leistung bieten wir derzeit nicht an. Übersicht aller aktuellen Leistungen von Oberholz Immobilien."/>
<style>
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f9;color:#1b2430}
  main{max-width:40rem;margin:12vh auto;padding:2rem;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:.75rem}
  h1{font-size:1.5rem;margin:0 0 .75rem}
  p{line-height:1.55;margin:0 0 1.25rem}
  a{color:#223a66;font-weight:600}
</style>
</head>
<body>
<main>
  <h1>Diese Leistung bieten wir nicht an</h1>
  <p>Die Seiten zu Immobilienbewertung durch Gutachter, Energieberatung und Energieausweis sind entfernt. Bitte nutzen Sie unsere aktuellen Leistungen.</p>
  <p><a href="/leistungen.html">Zur Leistungsübersicht</a> · <a href="/">Zur Startseite</a></p>
</main>
</body>
</html>
"""


def iter_html() -> list[Path]:
    paths: list[Path] = []
    index = ROOT / "index.html"
    if index.is_file():
        paths.append(index)
    public = ROOT / "public"
    for dirpath, _dirs, files in os.walk(public):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)
    return paths


def remove_anchor_or_img(html: str, src: str) -> str:
    html = re.sub(
        rf'<a\b[^>]*>\s*<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>\s*</a>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(rf'<img\b[^>]*\bsrc="{re.escape(src)}"[^>]*/?>', "", html, flags=re.I)
    return html


def remove_bmwi_logos(html: str) -> str:
    # Desktop: <li class="d-none d-lg-block"><img ... bmwi ...></li>
    html = re.sub(
        r'<li\b[^>]*class="[^"]*d-none d-lg-block[^"]*"[^>]*>\s*'
        r'<img\b[^>]*bmwi_eneffi[^>]*/?>\s*</li>',
        "",
        html,
        flags=re.I,
    )
    # Mobile / bare img
    html = re.sub(
        r'<img\b[^>]*bmwi_eneffi[^>]*/?>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<img\b[^>]*alt="[^"]*Deutschland machts effizient[^"]*"[^>]*/?>',
        "",
        html,
        flags=re.I,
    )
    return html


def remove_bafa_topbar(html: str) -> str:
    # Full column with BAFA claim
    html = re.sub(
        r'<div class="col ms-auto text-end d-none d-xl-block">\s*'
        r'<div class="text-white my-md-1">\s*'
        r"[^<]*BAFA-zertifizierte Energieberater[^<]*"
        r"</div>\s*</div>",
        "",
        html,
        flags=re.I,
    )
    # Fallback: just the text node variants
    html = html.replace(
        "🏆 BAFA-zertifizierte Energieberater | 🇩🇪 Förderexperten des Bundes",
        "",
    )
    html = html.replace(
        "BAFA-zertifizierte Energieberater | Förderexperten des Bundes",
        "",
    )
    return html


def remove_service_nav_items(html: str) -> str:
    for path in SERVICE_PATHS:
        # Dropdown items (may span nested spans)
        html = re.sub(
            rf'<a\b[^>]*href="{re.escape(path)}"[^>]*>[\s\S]*?</a>',
            "",
            html,
            flags=re.I,
        )
        # List/card wrappers that only contain the removed link already gone;
        # also strip plain href leftovers in overview cards.
        html = html.replace(path, "/leistungen.html")
    return html


def remove_bekannt_aus_section(html: str) -> str:
    """Drop the 'bekannt aus' media logo strip (ARD, Galileo, RTL, …)."""
    # Heading + following fluid container with media logos
    pat = re.compile(
        r'<div class="[^"]*">\s*'
        r'<div class="[^"]*text-center text-muted text-sm[^"]*">\s*'
        r"Oberholz Immobilien ist bekannt aus:\s*</div>\s*</div>\s*</div>\s*"
        r'<div class="container-fluid">\s*'
        r'<div class="row d-flex justify-content-around">[\s\S]*?</div>\s*</div>',
        re.I,
    )
    html = pat.sub("", html)
    # Fallback: any remaining "bekannt aus" line
    html = re.sub(
        r'<div class="[^"]*text-center text-muted text-sm[^"]*">\s*'
        r"Oberholz Immobilien ist bekannt aus:\s*</div>",
        "",
        html,
        flags=re.I,
    )
    return html


def remove_media_and_immoscout(html: str) -> str:
    html = remove_bekannt_aus_section(html)
    for src in MEDIA_SRCS:
        html = remove_anchor_or_img(html, src)
    # ImmoScout portal links without logo
    html = re.sub(
        r'<a\b[^>]*href="https://portal\.immobilienscout24\.de/[^"]*"[^>]*>[\s\S]*?</a>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<a\b[^>]*href="https://www\.immobilienscout24\.de/[^"]*"[^>]*>[\s\S]*?</a>',
        "",
        html,
        flags=re.I,
    )
    return html


def clean_empty_partner_cols(html: str) -> str:
    # Empty columns left after logo removal in media grids
    html = re.sub(
        r'<div class="col-md-1 col-3[^"]*"></div>\s*',
        "",
        html,
        flags=re.I,
    )
    return html


def patch_footer_copy(html: str) -> str:
    html = html.replace(FOOTER_OLD, FOOTER_NEW)
    html = html.replace(FOOTER_OLD_ALT, FOOTER_NEW)
    # Broader footer variants
    html = re.sub(
        r"Die <strong>Oberholz Immobilien</strong> verbinden Immobilienvermittlung mit "
        r"(?:einzigartiger Energiekompetenz|fundierter Markt- und Gutachterkompetenz)\."
        r"[^<]*?(?:Bochum und Umgebung|Bochum und Münster)\.",
        FOOTER_NEW.replace("<strong>", "<strong>").replace("</strong>", "</strong>"),
        html,
        flags=re.I,
    )
    html = html.replace("in Bochum und Umgebung.", "in Essen und Umgebung.")
    html = html.replace("in Bochum und Münster.", "in Essen und Umgebung.")
    html = html.replace(", in Bochum und Umgebung", ", in Essen und Umgebung")
    html = html.replace(", in Bochum und Münster", ", in Essen und Umgebung")
    return html


def patch_homepage_chrome(html: str, path: Path) -> str:
    if path.resolve() != (ROOT / "index.html").resolve():
        return html

    html = html.replace(
        "<title>Immobilienmakler Bochum | Oberholz Immobilien – auch Münster</title>",
        "<title>Immobilienmakler Essen | Oberholz Immobilien – auch Münster &amp; Bochum</title>",
    )
    html = html.replace(
        'content="Immobilienmakler Bochum | Oberholz Immobilien – auch Münster"',
        'content="Immobilienmakler Essen | Oberholz Immobilien – auch Münster &amp; Bochum"',
    )
    html = html.replace(
        "Oberholz Immobilien: Verkauf, Vermietung, Rückmietverkauf und Marktwertermittlung "
        "durch zertifizierten Immobiliengutachter. Schwerpunkt Bochum – mit Zentrale in Münster.",
        "Oberholz Immobilien: Verkauf und Vermietung mit Schwerpunkt Essen – "
        "persönlich, transparent und vor Ort. Auch in Münster und Bochum.",
    )
    html = html.replace(
        "Schwerpunkt Bochum – mit Zentrale in Münster.",
        "Schwerpunkt Essen – auch Münster und Bochum.",
    )
    html = html.replace(
        "Ihr Immobilienmakler für Bochum",
        "Ihr Immobilienmakler für Essen",
    )
    html = html.replace(
        "in Bochum und Umgebung",
        "in Essen und Umgebung",
    )
    # Remove gutachter claims from homepage meta leftovers
    html = re.sub(
        r"Marktwertermittlung durch zertifizierten Immobiliengutachter\.?\s*",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"durch zertifizierten Immobiliengutachter\.?\s*",
        "",
        html,
        flags=re.I,
    )
    return html


def remove_kontakt_bewertung_option(html: str) -> str:
    html = re.sub(
        r'<option\b[^>]*value="Immobilienbewertung"[^>]*>[\s\S]*?</option>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<option\b[^>]*value="Energieberatung"[^>]*>[\s\S]*?</option>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<option\b[^>]*>\s*Immobilienbewertung\s*</option>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<option\b[^>]*>\s*Energieberatung\s*</option>',
        "",
        html,
        flags=re.I,
    )
    return html


def remove_leistungen_cards(html: str, path: Path) -> str:
    if path.name not in {"leistungen.html"} and "leistungen" not in path.parts[-2:]:
        # Still strip cards that deep-link to retired services on any page
        pass

    # Service cards / feature blocks linking to retired pages – remove enclosing column if simple
    for slug in ("immobilienbewertung", "energieberatung", "energieausweis-kostenlos"):
        html = re.sub(
            rf'<div class="col[^"]*">\s*<a\b[^>]*href="/leistungen/{slug}\.html"[^>]*>[\s\S]*?</a>\s*</div>',
            "",
            html,
            flags=re.I,
        )
        html = re.sub(
            rf'<div class="[^"]*feature[^"]*"[^>]*>[\s\S]*?href="/leistungen/{slug}\.html"[\s\S]*?</div>\s*</div>',
            "",
            html,
            flags=re.I,
        )
    return html


def strip_inline_rainbow(html: str) -> str:
    # Soften remaining inline rainbow rules (CSS override already hides them)
    html = re.sub(
        r"background:\s*linear-gradient\(90deg,\s*#006d32[^;]*\);?",
        "background: none;",
        html,
        flags=re.I,
    )
    return html


def process(html: str, path: Path) -> str:
    html = remove_bmwi_logos(html)
    html = remove_bafa_topbar(html)
    html = remove_media_and_immoscout(html)
    html = clean_empty_partner_cols(html)
    html = remove_service_nav_items(html)
    html = remove_kontakt_bewertung_option(html)
    html = remove_leistungen_cards(html, path)
    html = patch_footer_copy(html)
    html = patch_homepage_chrome(html, path)
    html = strip_inline_rainbow(html)
    return html


def write_stubs() -> None:
    for path in RETIRED_PAGES:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB_HTML, encoding="utf-8")


def main() -> None:
    started = time.time()
    write_stubs()
    seen = changed = 0
    for path in iter_html():
        seen += 1
        # Stubs already written; still process if they get walked (idempotent)
        try:
            original = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            print("fail read", path, exc, flush=True)
            continue
        updated = process(original, path)
        if updated != original:
            try:
                path.write_text(updated, encoding="utf-8")
                changed += 1
            except OSError as exc:
                print("fail write", path, exc, flush=True)
        if seen % 2000 == 0:
            print(
                f"progress {seen} changed={changed} elapsed={time.time()-started:.0f}s",
                flush=True,
            )
    print(
        "DONE",
        {"seen": seen, "changed": changed},
        f"elapsed={time.time()-started:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
