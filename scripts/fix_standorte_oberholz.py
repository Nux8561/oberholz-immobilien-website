# -*- coding: utf-8 -*-
"""
Standort-Fix: IE-Städte -> Oberholz Münster / Essen / Bochum
- Desktop-Kontakt-Dropdown
- Mobile-Kontakt-Liste
- Standort-Tabelle auf kontakt-aufnehmen
- Neue Standortseiten anlegen
- Alte Stadt-Seiten auf Kontakt umleiten
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]

PIN_SVG = (
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" class="fs-5 mt-n1 align-middle" '
    'style="width: 1em; height: 1em;"><title>Standort Icon</title>'
    '<path d="M15 10.5C15 12.1569 13.6569 13.5 12 13.5C10.3431 13.5 9 12.1569 9 10.5C9 8.84315 10.3431 7.5 12 7.5C13.6569 7.5 15 8.84315 15 10.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M19.5 10.5C19.5 17.6421 12 21.75 12 21.75C12 21.75 4.5 17.6421 4.5 10.5C4.5 6.35786 7.85786 3 12 3C16.1421 3 19.5 6.35786 19.5 10.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

EXT_SVG = (
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" class="fs-5 mt-n1 align-middle" '
    'style="width: 1em; height: 1em;"><title>Externer Link Icon</title>'
    '<path d="M13.5 6H5.25C4.00736 6 3 7.00736 3 8.25V18.75C3 19.9926 4.00736 21 5.25 21H15.75C16.9926 21 18 19.9926 18 18.75V10.5M7.5 16.5L21 3M21 3L15.75 3M21 3V8.25" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

FACE = (
    '<div class="facepile-container"> '
    '<img src="/media/facepile/oberholz_facepile.jpg" alt="Michael Oberholz" '
    'title="Michael Oberholz" loading="lazy" class="face-circle"> </div>'
)

CITIES = [
    {
        "slug": "muenster",
        "name": "Münster",
        "region": "Münster und Münsterland",
        "blurb": "Ihr Immobilienmakler in Münster und im Münsterland – Verkauf, Vermietung und Wertermittlung vor Ort.",
    },
    {
        "slug": "essen",
        "name": "Essen",
        "region": "Essen und Ruhrgebiet",
        "blurb": "Ihr Immobilienmakler in Essen und im Ruhrgebiet – Verkauf, Vermietung und Wertermittlung vor Ort.",
    },
    {
        "slug": "bochum",
        "name": "Bochum",
        "region": "Bochum und Umgebung",
        "blurb": "Ihr Immobilienmakler in Bochum und Umgebung – Verkauf, Vermietung und Wertermittlung vor Ort.",
    },
]

OLD_SLUGS = [
    "hamburg",
    "duesseldorf",
    "hannover",
    "stuttgart",
    "villingen-schwenningen",
    "frankfurt-am-main",
    "muenchen",
]

# --- Desktop nav: replace 7-city block with 3 cities (keep column wrapper) ---
DESKTOP_CITY_RE = re.compile(
    r'<a class="dropdown-item ?" href="/kontakt/immobilienmakler-hamburg\.html"[^>]*>'
    r'.*?'
    r'Immobilienmakler München</span></a>',
    re.S,
)

def desktop_cities_html(space: bool) -> str:
    sp = " " if space else ""
    links = []
    for c in CITIES:
        links.append(
            f'<a class="dropdown-item{sp}" href="/kontakt/immobilienmakler-{c["slug"]}.html" '
            f'title="Immobilienmakler {c["name"]}"> '
            f'<span class="menu-label">Immobilienmakler {c["name"]}</span></a>'
        )
    # keep empty second column structure for layout consistency
    return "".join(links) + '</div><div class="col-12 col-md-6">'


# Old block included mid-column break - our regex ends at München, so we need
# to include the column break in the match. Looking at saved block:
# hamburg...hannover</a></div><div class="col-12 col-md-6">stuttgart...muenchen</a>
DESKTOP_CITY_RE2 = re.compile(
    r'<a class="dropdown-item ?" href="/kontakt/immobilienmakler-hamburg\.html"[^>]*>'
    r'.*?'
    r'<a class="dropdown-item ?" href="/kontakt/immobilienmakler-muenchen\.html"[^>]*>'
    r'.*?Immobilienmakler München</span></a>',
    re.S,
)

MOBILE_CITY_RE = re.compile(
    r'<li class="my-3 ?"><a class="" href="/kontakt/immobilienmakler-hamburg\.html"[^>]*>'
    r'Immobilienmakler Hamburg</a></li>'
    r'(?:<li class="my-3 ?"><a class="" href="/kontakt/immobilienmakler-[a-z-]+\.html"[^>]*>'
    r'Immobilienmakler [^<]+</a></li>)+',
    re.S,
)


def mobile_cities_html() -> str:
    parts = []
    for c in CITIES:
        parts.append(
            f'<li class="my-3 "><a class="" href="/kontakt/immobilienmakler-{c["slug"]}.html" '
            f'title="Immobilienmakler {c["name"]}">Immobilienmakler {c["name"]}</a></li>'
        )
    return "".join(parts)


def standort_row(region: str, name: str, slug: str) -> str:
    return (
        f"<tr> <td> {region} {FACE} </td> "
        f"<td>{PIN_SVG} {name}</td> "
        f'<td class="text-right d-none d-md-table-cell"><span class="badge badge-ort p-2">Vor Ort</span></td> '
        f'<td> <a href="/kontakt/immobilienmakler-{slug}.html" class="table-link">'
        f"{EXT_SVG} Immobilienmakler {name}</a> </td> </tr>"
    )


NEW_TBODY = (
    "<tbody> "
    + standort_row("Münster und Münsterland", "Münster", "muenster")
    + standort_row("Essen und Ruhrgebiet", "Essen", "essen")
    + standort_row("Bochum und Umgebung", "Bochum", "bochum")
    + " </tbody>"
)

TBODY_RE = re.compile(r"<tbody>.*?</tbody>", re.S)

# Safety: individual href+label swaps if block match fails
HREF_MAP = {
    "/kontakt/immobilienmakler-hamburg.html": "/kontakt/immobilienmakler-muenster.html",
    "/kontakt/immobilienmakler-duesseldorf.html": "/kontakt/immobilienmakler-essen.html",
    "/kontakt/immobilienmakler-hannover.html": "/kontakt/immobilienmakler-bochum.html",
    "/kontakt/immobilienmakler-stuttgart.html": "/kontakt/immobilienmakler-muenster.html",
    "/kontakt/immobilienmakler-villingen-schwenningen.html": "/kontakt/immobilienmakler-essen.html",
    "/kontakt/immobilienmakler-frankfurt-am-main.html": "/kontakt/immobilienmakler-bochum.html",
    "/kontakt/immobilienmakler-muenchen.html": "/kontakt/immobilienmakler-muenster.html",
}

LABEL_MAP = [
    ("Immobilienmakler Hamburg", "Immobilienmakler Münster"),
    ("Immobilienmakler Düsseldorf", "Immobilienmakler Essen"),
    ("Immobilienmakler Duesseldorf", "Immobilienmakler Essen"),
    ("Immobilienmakler Hannover", "Immobilienmakler Bochum"),
    ("Immobilienmakler Stuttgart", "Immobilienmakler Münster"),
    ("Immobilienmakler Villingen-Schwenningen", "Immobilienmakler Essen"),
    ("Immobilienmakler Frankfurt am Main", "Immobilienmakler Bochum"),
    ("Immobilienmakler München", "Immobilienmakler Münster"),
    ("Immobilienmakler M&uuml;nchen", "Immobilienmakler Münster"),
]

TEXT_FIXES = [
    (
        "Wir sind für Sie da – bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "Wir sind für Sie da – persönlich vor Ort in Münster, Essen und Bochum.",
    ),
    (
        "Wir sind für Sie da - bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "Wir sind für Sie da – persönlich vor Ort in Münster, Essen und Bochum.",
    ),
    (
        "Ihre Immobilienmakler für ganz Deutschland",
        "Ihr Immobilienmakler für Münster, Essen und Bochum",
    ),
]


def patch_html_text(text: str) -> tuple[str, dict]:
    stats = {"desktop": 0, "mobile": 0, "tbody": 0, "href": 0, "label": 0, "text": 0}

    def desk_repl(m: re.Match) -> str:
        stats["desktop"] += 1
        space = "dropdown-item " in m.group(0)[:40]
        return desktop_cities_html(space)

    text2, n = DESKTOP_CITY_RE2.subn(desk_repl, text)
    text = text2
    if n == 0:
        text2, n = DESKTOP_CITY_RE.subn(desk_repl, text)
        text = text2

    def mob_repl(m: re.Match) -> str:
        stats["mobile"] += 1
        return mobile_cities_html()

    text, n = MOBILE_CITY_RE.subn(mob_repl, text)

    # Only replace tbody if it still mentions wrong cities (Standort table)
    if "Baden-Württemberg" in text or "Villingen-Schwenningen" in text or "Immobilienmakler Stuttgart" in text:
        def tb_repl(m: re.Match) -> str:
            body = m.group(0)
            if any(
                x in body
                for x in ("Stuttgart", "Hamburg", "München", "Villingen", "Frankfurt", "Hannover", "Düsseldorf", "Berlin", "Augsburg", "Nürnberg")
            ):
                stats["tbody"] += 1
                return NEW_TBODY
            return body

        text = TBODY_RE.sub(tb_repl, text)

    for old, new in HREF_MAP.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            stats["href"] += c

    for old, new in LABEL_MAP:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            stats["label"] += c

    for old, new in TEXT_FIXES:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            stats["text"] += c

    return text, stats


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for p in [ROOT / "index.html", *ROOT.glob("*.html")]:
        if p.is_file():
            files.append(p)
    pub = ROOT / "public"
    if pub.is_dir():
        files.extend(pub.rglob("*.html"))
    # dedupe
    seen = set()
    out = []
    for f in files:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def needs_scan(raw: bytes) -> bool:
    needles = [
        b"immobilienmakler-hamburg.html",
        b"immobilienmakler-stuttgart.html",
        b"immobilienmakler-muenchen.html",
        b"immobilienmakler-duesseldorf.html",
        b"immobilienmakler-hannover.html",
        b"immobilienmakler-frankfurt",
        b"immobilienmakler-villingen",
        b"Baden-W",
        b"Immobilienmakler Stuttgart",
        b"Immobilienmakler Hamburg",
        b"bundesweit und auch regional",
    ]
    return any(n in raw for n in needles)


def create_standort_pages() -> None:
    src = ROOT / "public" / "kontakt" / "immobilienmakler-stuttgart.html"
    if not src.exists():
        print("WARN: stuttgart template missing")
        return
    base = src.read_text(encoding="utf-8", errors="ignore")
    kontakt = ROOT / "public" / "kontakt"

    # City-specific replacements from Stuttgart template
    for c in CITIES:
        text = base
        # URL/slug first
        text = text.replace("immobilienmakler-stuttgart", f"immobilienmakler-{c['slug']}")
        text = text.replace("/kontakt/immobilienmakler-stuttgart.html", f"/kontakt/immobilienmakler-{c['slug']}.html")
        # Names (order matters for compounds)
        text = text.replace("Villingen-Schwenningen", c["name"])  # leftover nav may get fixed later
        text = text.replace("Stuttgart", c["name"])
        text = text.replace("stuttgart", c["slug"])
        text = text.replace("Baden-Württemberg", c["region"])
        text = text.replace("Baden-Wuerttemberg", c["region"])

        # Titles / meta polish
        text = text.replace(
            f"Immobilienmakler {c['name']} | Oberholz",
            f"Immobilienmakler {c['name']} | Oberholz Immobilien",
        )
        # Canonical
        text = re.sub(
            r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="/kontakt/immobilienmakler-{c["slug"]}.html">',
            text,
            count=1,
        )

        out = kontakt / f"immobilienmakler-{c['slug']}.html"
        out.write_text(text, encoding="utf-8")
        print("created", out.relative_to(ROOT))

        # Optional: folder with subpages - skip for now (nav points to main page)


def redirect_old_city_pages() -> None:
    """Replace old IE city hub pages with redirect to matching Oberholz standort."""
    mapping = {
        "hamburg": "muenster",
        "hannover": "muenster",
        "stuttgart": "muenster",
        "muenchen": "muenster",
        "duesseldorf": "essen",
        "villingen-schwenningen": "essen",
        "frankfurt-am-main": "bochum",
    }
    kontakt = ROOT / "public" / "kontakt"
    for old, new in mapping.items():
        path = kontakt / f"immobilienmakler-{old}.html"
        if not path.exists():
            continue
        target = f"/kontakt/immobilienmakler-{new}.html"
        html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Weiterleitung | Oberholz Immobilien</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0;url={target}">
<script>location.replace({target!r});</script>
</head>
<body>
<p>Dieser Standort gehört zu Oberholz Immobilien in Münster, Essen und Bochum.
<a href="{target}">Weiter zur Standortseite</a>.</p>
</body>
</html>
"""
        path.write_text(html, encoding="utf-8")
        print("redirect", path.name, "->", target)


def main() -> None:
    print("Creating standort pages...")
    create_standort_pages()

    print("Redirecting old city hubs...")
    redirect_old_city_pages()

    files = iter_html_files()
    print(f"Scanning {len(files)} HTML files...")
    changed = 0
    scanned = 0
    totals = {"desktop": 0, "mobile": 0, "tbody": 0, "href": 0, "label": 0, "text": 0}

    for path in files:
        try:
            raw = path.read_bytes()
        except OSError as e:
            print("skip", path, e)
            continue
        if not needs_scan(raw):
            continue
        scanned += 1
        text = raw.decode("utf-8", errors="ignore")
        new_text, stats = patch_html_text(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            for k, v in stats.items():
                totals[k] += v
            if changed <= 8 or path.name in ("index.html", "kontakt-aufnehmen.html"):
                print("patched", path.relative_to(ROOT), stats)

    print("DONE scanned", scanned, "changed", changed, "totals", totals)


if __name__ == "__main__":
    main()
