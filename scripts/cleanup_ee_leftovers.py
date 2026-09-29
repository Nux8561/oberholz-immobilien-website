"""Remove EE leftovers; only touch HTML files that still contain needles."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GOOGLE_REVIEWS = (
    "https://www.google.com/maps/place/Oberholz+Immobilien/"
    "@51.9735915,7.6248835,17z/data=!4m6!3m5!1s0x47b9bb4567805459:0xa08f5b6274a4201c"
    "!8m2!3d51.9735915!4d7.6248835!16s%2Fg%2F11shxgxbpq"
)
IS24_LIST = "https://portal.immobilienscout24.de/ergebnisliste/82828525"
PLATZHIRSCH = "https://www.platzhirsch-online.de/"
OBERHOLZ_HOME = "https://www.oberholz-immobilien.com"
EMAIL = "mail@oberholz-immobilien.com"

RATING = "5.0"
REVIEW_COUNT = "9"

IMPRESSUM_LEGAL_HTML = """<h3><strong>Angaben gem. § 5 TMG:</strong></h3><hr>
<p><strong>Oberholz Immobilien</strong></p>
<p>Wichernstr. 29<br>D-48147 Münster<br><br>
Tel. +49 (0)251 – 28 42 90 90<br>
Fax +49 (0)251 – 28 42 90 91<br>
E-Mail: <a href="mailto:mail@oberholz-immobilien.com">mail@oberholz-immobilien.com</a><br>
(Impressum-Kontakt: <a href="mailto:info@sv-oberholz.de">info@sv-oberholz.de</a>)<br><br>
Bürotermine nach Vereinbarung!<br><br>
Finanzamt Münster-Innenstadt<br>
USt.-Id-Nr. DE297711149<br><br>
Berufsaufsichtsbehörde: Stadt Münster, Ordnungsamt, Klemensstr. 10, Münster<br><br>
Eine Vermögensschadenhaftpflichtversicherung besteht bei der ERGO Versicherungsgruppe AG, Victoriaplatz 2, 40198 Düsseldorf<br><br>
Eine Vertrauensschadenhaftpflichtversicherung besteht über den Immobilienverband Deutschlands IVD bei der ERGO Versicherungsgruppe AG, Victoriaplatz 2, 40198 Düsseldorf</p>
<p>Verbraucherinformationen: Online-Streitbeilegung gemäß Art. 14 Abs. 1 ODR-VO: Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit:
<a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener noreferrer">https://ec.europa.eu/consumers/odr</a></p>
<p>Verbraucherinformation zur Schlichtungsstelle:<br>
Ombudsmann Immobilien im IVD<br>
Wolfgang Ball – Ombudsstelle –<br>
Littenstraße 10, 10179 Berlin<br>
Fax: 030 / 27 57 26 78<br>
E-Mail: info@ombudsmann-immobilien.net<br>
Internet: <a href="http://www.ombudsmann-immobilien.net" target="_blank" rel="noopener noreferrer">http://www.ombudsmann-immobilien.net</a></p>
</div>
"""

ORIGIN_COLLAPSE_NEW = (
    '<div class="collapse mt-2" id="typeform-rating-origin-collapse">'
    '<div class="small text-start text-muted">'
    "<p>Die angezeigten Bewertungen stammen aus dem <strong>öffentlichen Google-Unternehmensprofil</strong> "
    "von Oberholz Immobilien (Wichernstraße 29, 48147 Münster).</p>"
    "<p><mark>Es handelt sich um echte Google-Kundenrezensionen – unverändert und öffentlich nachvollziehbar.</mark></p>"
    f'<p><a href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener noreferrer">Alle Google-Bewertungen ansehen</a></p>'
    "</div></div></div>"
)

SKIP_DIR_NAMES = {
    "node_modules",
    "dist",
    ".git",
    "analysis",
    "reference",
    "screenshots",
    "theme",
    "assets",
    "scripts",
    "src",
}

NEEDLES = (
    b"ee-experten",
    b"3106",
    b"3.106",
    b"mattomedia",
    b"medienfeuer",
    b"immobilienwert-experten",
    b"broschuere_ee",
    b"easyfit-villingen",
    b"info@ee-experten",
    b"HRB 728245",
    b"DE359323139",
    b"Von-Liebig-Str",
)


def iter_html() -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        # skip public/theme
        rel = Path(dirpath).relative_to(ROOT).parts
        if len(rel) >= 2 and rel[0] == "public" and rel[1] == "theme":
            dirnames[:] = []
            continue
        for name in filenames:
            if name.endswith(".html"):
                out.append(Path(dirpath) / name)
    return out


def replace_all(html: str) -> str:
    simple = [
        ("https://www.ee-experten.com/erfahrungen-und-bewertungen.html?bundesland=immo", GOOGLE_REVIEWS),
        ("https://www.ee-experten.com/erfahrungen-und-bewertungen.html", GOOGLE_REVIEWS),
        ("https://www.ee-experten.com", OBERHOLZ_HOME),
        ("http://www.ee-experten.com", OBERHOLZ_HOME),
        ("https://www.immobilienscout24.de/anbieter/profil/ee-experten-gmbh", IS24_LIST),
        ("https://www.immowelt.de/profil/ee-experten", OBERHOLZ_HOME),
        ("https://www.immobilienwert-experten.com", OBERHOLZ_HOME),
        ("http://www.immobilienwert-experten.com", OBERHOLZ_HOME),
        ("info@ee-experten.de", EMAIL),
        ("www.medienfeuer.de", "www.platzhirsch-online.de"),
        ("https://www.medienfeuer.de/", PLATZHIRSCH),
        ("https://www.medienfeuer.de", PLATZHIRSCH),
        ("www.mattomedia.de", "www.platzhirsch-online.de"),
        ("https://www.mattomedia.de/", PLATZHIRSCH),
        ("https://www.mattomedia.de", PLATZHIRSCH),
        ("Medienfeuer®", "Platzhirsch Online"),
        ("Medienfeuer", "Platzhirsch Online"),
        (".mattomedia®", "Platzhirsch Online"),
        (".mattomedia", "Platzhirsch Online"),
        ("mattomedia Werbeagentur", "Platzhirsch Online"),
        ("Unsere Agentur mattomedia", "Unsere Agentur Platzhirsch Online"),
        ("/media/broschuere_ee-immobilien_web.pdf", "/media/broschuere_energieberatung-oberholz.pdf"),
        ("/media/broschuere_ee-experten_web.pdf", "/media/broschuere_energieberatung-oberholz.pdf"),
        ("broschuere_ee-immobilien_web.pdf", "broschuere_energieberatung-oberholz.pdf"),
        ("broschuere_ee-experten_web.pdf", "broschuere_energieberatung-oberholz.pdf"),
        ("https://easyfit-villingen.de/firmenfitness-ee-experten/", PLATZHIRSCH),
        ("EE-Experten GmbH", "Oberholz Immobilien"),
        ("EE-Experten", "Oberholz Immobilien"),
        ("ee-experten GmbH", "Oberholz Immobilien"),
    ]
    for old, new in simple:
        if old in html:
            html = html.replace(old, new)

    rating_pairs = [
        (r'("reviewCount"\s*:\s*)3106([,}])', rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r'("reviewCount"\s*:\s*")3106(")', rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r"3106\u00a0Bewertungen", f"{REVIEW_COUNT}&nbsp;Bewertungen"),
        (r"3\.106\u00a0Bewertungen", f"{REVIEW_COUNT}&nbsp;Bewertungen"),
        (r"3106&nbsp;Bewertungen", f"{REVIEW_COUNT}&nbsp;Bewertungen"),
        (r"(Basierend auf <strong>)3106(</strong> echten Bewertungen)", rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r"(Basierend auf <strong>)3\.106(</strong> echten Bewertungen)", rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r"(>)3106(</span>\s*Bewertungen)", rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r"(>)3106(&nbsp;Bewertungen)", rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r"(>)3\.106( Bewertungen)", rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r'("ratingCount"\s*:\s*")3106(")', rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r'("ratingCount"\s*:\s*)3106([,}])', rf"\g<1>{REVIEW_COUNT}\g<2>"),
        (r'("ratingValue"\s*:\s*")4\.9(")', rf"\g<1>{RATING}\g<2>"),
        (r'("ratingValue"\s*:\s*)4\.9([,}])', rf"\g<1>{RATING}\g<2>"),
        (r'(<span class="fs-3 fw-bold">)4\.9(</span>)', rf"\g<1>{RATING}\g<2>"),
        (r"(>)4\.9/5(</strong>)", rf"\g<1>{RATING}/5\g<2>"),
        (r">4\.9 / 5<", f">{RATING} / 5<"),
        (r"fa-star-half-stroke", "fa-star"),
    ]
    for pattern, repl in rating_pairs:
        html = re.sub(pattern, repl, html, flags=re.I)

    html = re.sub(
        r'<div class="collapse mt-2" id="typeform-rating-origin-collapse">[\s\S]*?</div>\s*</div>',
        ORIGIN_COLLAPSE_NEW,
        html,
        count=1,
    )

    html = re.sub(
        r'title="Erfahrungen und Bewertungen der Oberholz Immobilien"',
        'title="Google-Bewertungen von Oberholz Immobilien"',
        html,
    )
    html = re.sub(
        r">Erfahrungen\s*(?:&amp;|&)\s*Bewertungen<",
        ">Google-Bewertungen<",
        html,
    )
    return html


def patch_impressum(html: str) -> str:
    pattern = re.compile(
        r"(?s)<h3><strong>Angaben gem.*?</div>\s*<div class=\"col-md-6 text-break\">\s*<h3><strong>Konzeption",
    )
    m = pattern.search(html)
    if not m:
        return html
    return (
        html[: m.start()]
        + IMPRESSUM_LEGAL_HTML
        + '<div class="col-md-6 text-break"><h3><strong>Konzeption'
        + html[m.end() :]
    )


def patch_datenschutz(html: str) -> str:
    html = html.replace("info@ee-experten.de", EMAIL)
    html = html.replace("ee-experten.de", "oberholz-immobilien.com")
    html = html.replace("EE-Experten GmbH", "Oberholz Immobilien")
    html = html.replace("EE-Experten", "Oberholz Immobilien")
    return html


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    files = iter_html()
    print(f"html_files={len(files)}", flush=True)
    changed = 0
    scanned_hit = 0
    for i, path in enumerate(files, 1):
        if i % 500 == 0:
            print(f"progress {i}/{len(files)} changed={changed}", flush=True)
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if not any(n in raw for n in NEEDLES):
            continue
        scanned_hit += 1
        try:
            html = raw.decode("utf-8")
        except UnicodeDecodeError:
            html = raw.decode("utf-8", errors="replace")
        html2 = replace_all(html)
        if path.name == "impressum.html":
            html2 = patch_impressum(html2)
        if path.name == "datenschutzerklaerung.html":
            html2 = patch_datenschutz(html2)
        if html2 != html:
            path.write_text(html2, encoding="utf-8", newline="")
            changed += 1
            if changed <= 20 or path.name in {
                "index.html",
                "impressum.html",
                "datenschutzerklaerung.html",
            }:
                print(f"patched {path.relative_to(ROOT)}", flush=True)
    print(f"DONE hits={scanned_hit} changed={changed}", flush=True)


if __name__ == "__main__":
    main()
