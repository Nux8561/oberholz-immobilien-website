# -*- coding: utf-8 -*-
"""Schneller Standort-Fix: zuerst Kernseiten, dann nur rg-Treffer."""
from __future__ import annotations

import re
import subprocess
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
    {"slug": "muenster", "name": "Münster", "region": "Münster und Münsterland"},
    {"slug": "essen", "name": "Essen", "region": "Essen und Ruhrgebiet"},
    {"slug": "bochum", "name": "Bochum", "region": "Bochum und Umgebung"},
]

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
    ("Immobilienmakler Hannover", "Immobilienmakler Bochum"),
    ("Immobilienmakler Stuttgart", "Immobilienmakler Münster"),
    ("Immobilienmakler Villingen-Schwenningen", "Immobilienmakler Essen"),
    ("Immobilienmakler Frankfurt am Main", "Immobilienmakler Bochum"),
    ("Immobilienmakler München", "Immobilienmakler Münster"),
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
        "<strong>Wir sind für Sie da</strong> – bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "<strong>Wir sind für Sie da</strong> – persönlich vor Ort in Münster, Essen und Bochum.",
    ),
    (
        "<strong>Wir sind für Sie da</strong> - bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "<strong>Wir sind für Sie da</strong> – persönlich vor Ort in Münster, Essen und Bochum.",
    ),
    (
        "bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "persönlich vor Ort in Münster, Essen und Bochum.",
    ),
]

BAD_TBODY_MARKERS = (
    "Stuttgart",
    "Hamburg",
    "München",
    "Villingen",
    "Frankfurt",
    "Hannover",
    "Düsseldorf",
    "Berlin",
    "Augsburg",
    "Nürnberg",
    "Baden-Württemberg",
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
    return "".join(links) + '</div><div class="col-12 col-md-6">'


def mobile_cities_html() -> str:
    return "".join(
        f'<li class="my-3 "><a class="" href="/kontakt/immobilienmakler-{c["slug"]}.html" '
        f'title="Immobilienmakler {c["name"]}">Immobilienmakler {c["name"]}</a></li>'
        for c in CITIES
    )


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


def patch_html_text(text: str) -> tuple[str, dict]:
    stats = {"desktop": 0, "mobile": 0, "tbody": 0, "href": 0, "label": 0, "text": 0}

    def desk_repl(m: re.Match) -> str:
        stats["desktop"] += 1
        space = "dropdown-item " in m.group(0)[:40]
        return desktop_cities_html(space)

    text, _ = DESKTOP_CITY_RE2.subn(desk_repl, text)

    def mob_repl(_: re.Match) -> str:
        stats["mobile"] += 1
        return mobile_cities_html()

    text, _ = MOBILE_CITY_RE.subn(mob_repl, text)

    def tb_repl(m: re.Match) -> str:
        body = m.group(0)
        # Never rewrite tax / GrESt tables (headers sit in surrounding <table>).
        start = m.start()
        window = text[max(0, start - 400) : start + 80]
        if "Steuersatz" in window or "Grunderwerbsteuer" in window:
            return body
        if any(x in body for x in BAD_TBODY_MARKERS):
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


def create_standort_pages() -> None:
    src = ROOT / "public" / "kontakt" / "immobilienmakler-stuttgart.html"
    if not src.exists():
        # maybe already redirected
        print("WARN: stuttgart template missing, trying hamburg")
        src = ROOT / "public" / "kontakt" / "immobilienmakler-hamburg.html"
    if not src.exists() or src.stat().st_size < 5000:
        print("ERROR: no usable city template")
        return

    base = src.read_text(encoding="utf-8", errors="ignore")
    # Detect source city
    if "Stuttgart" in base:
        src_name, src_slug, src_region = "Stuttgart", "stuttgart", "Baden-Württemberg"
    elif "Hamburg" in base:
        src_name, src_slug, src_region = "Hamburg", "hamburg", "Hamburg"
    else:
        print("ERROR: unknown template city")
        return

    kontakt = ROOT / "public" / "kontakt"
    for c in CITIES:
        text = base
        text = text.replace(f"immobilienmakler-{src_slug}", f"immobilienmakler-{c['slug']}")
        text = text.replace(src_name, c["name"])
        text = text.replace(src_slug, c["slug"])
        text = text.replace(src_region, c["region"])
        text = text.replace("ganz Baden-Württemberg", c["region"])
        text = re.sub(
            r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="/kontakt/immobilienmakler-{c["slug"]}.html">',
            text,
            count=1,
        )
        out = kontakt / f"immobilienmakler-{c['slug']}.html"
        out.write_text(text, encoding="utf-8")
        print("created", out.name, "bytes", out.stat().st_size)


def redirect_old_city_pages() -> None:
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
        # Don't overwrite if it's our source before copy - create pages first!
        target = f"/kontakt/immobilienmakler-{new}.html"
        html = (
            "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<title>Weiterleitung | Oberholz Immobilien</title>\n"
            '<meta name="robots" content="noindex, follow">\n'
            f'<link rel="canonical" href="{target}">\n'
            f'<meta http-equiv="refresh" content="0;url={target}">\n'
            f"<script>location.replace({target!r});</script>\n</head>\n<body>\n"
            f'<p>Weiter zu <a href="{target}">Oberholz Immobilien {new.title()}</a>.</p>\n'
            "</body>\n</html>\n"
        )
        path.write_text(html, encoding="utf-8")
        print("redirect", path.name, "->", target)


PRIORITY = [
    "index.html",
    "public/kontakt/kontakt-aufnehmen.html",
    "public/ueber-uns.html",
    "public/leistungen.html",
    "public/regionen.html",
    "public/impressum.html",
]


def rg_files() -> list[Path]:
    pattern = (
        "immobilienmakler-hamburg\\.html|immobilienmakler-stuttgart\\.html|"
        "immobilienmakler-muenchen\\.html|immobilienmakler-duesseldorf\\.html|"
        "immobilienmakler-hannover\\.html|immobilienmakler-frankfurt|"
        "immobilienmakler-villingen|Immobilienmakler Stuttgart|"
        "Baden-Württemberg|bundesweit und auch regional"
    )
    try:
        r = subprocess.run(
            ["rg", "-l", "--glob", "*.html", pattern, str(ROOT / "public"), str(ROOT / "index.html")],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(ROOT),
            timeout=120,
        )
        paths = []
        for line in (r.stdout or "").splitlines():
            line = line.strip()
            if line:
                paths.append(Path(line))
        print(f"rg found {len(paths)} files")
        return paths
    except Exception as e:
        print("rg failed:", e)
        return []


def patch_file(path: Path) -> dict | None:
    try:
        raw = path.read_bytes()
    except OSError as e:
        print("read fail", path, e)
        return None
    text = raw.decode("utf-8", errors="ignore")
    new_text, stats = patch_html_text(text)
    if new_text == text:
        return None
    path.write_text(new_text, encoding="utf-8")
    return stats


def main() -> None:
    print("=== 1) Create standort pages ===")
    create_standort_pages()

    print("=== 2) Patch priority pages ===")
    totals = {"desktop": 0, "mobile": 0, "tbody": 0, "href": 0, "label": 0, "text": 0}
    changed = 0
    for rel in PRIORITY:
        path = ROOT / rel
        if not path.exists():
            print("missing", rel)
            continue
        stats = patch_file(path)
        if stats:
            changed += 1
            for k, v in stats.items():
                totals[k] += v
            print("patched", rel, stats)

    print("=== 3) Redirect old hubs ===")
    redirect_old_city_pages()

    print("=== 4) Patch rg hits ===")
    files = rg_files()
    # also include new standort pages
    for c in CITIES:
        files.append(ROOT / "public" / "kontakt" / f"immobilienmakler-{c['slug']}.html")

    seen = set()
    for path in files:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        if not path.exists():
            continue
        # skip old redirect stubs (small)
        if path.name.startswith("immobilienmakler-") and path.stat().st_size < 2000:
            if any(x in path.name for x in ("hamburg", "stuttgart", "muenchen", "duesseldorf", "hannover", "frankfurt", "villingen")):
                continue
        stats = patch_file(path)
        if stats:
            changed += 1
            for k, v in stats.items():
                totals[k] += v
            if changed <= 20 or changed % 50 == 0:
                print("patched", path, stats)

    print("DONE changed", changed, "totals", totals)


if __name__ == "__main__":
    main()
