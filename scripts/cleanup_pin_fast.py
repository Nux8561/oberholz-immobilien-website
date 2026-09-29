"""Fast Service-PIN + leftover name cleanup; skip unchanged files quickly."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"node_modules", ".git", "dist", "assets", ".cursor"}

PIN_RE = re.compile(
    r'\s*<div class="text-center d-block">\s*'
    r'<span class="text-muted">Service-PIN:\s*'
    r'<strong class="text-md"[^>]*>[^<]*</strong>\s*'
    r"</span>\s*</div>",
    re.I,
)
PIN_SPAN_RE = re.compile(
    r'<span class="text-muted">\s*Service-PIN:\s*'
    r'<strong class="text-md"[^>]*>[^<]*</strong>\s*</span>',
    re.I,
)

REPLACEMENTS = (
    ("Kersten Streit", "Michael Oberholz"),
    ("Wolfgang Mayer", "Felix Lesch"),
    ("Axel Winkler", "Michael Penn"),
    ("René Mohr", "Pascal Kopp"),
    ("Rene Mohr", "Pascal Kopp"),
    ("Ren&eacute; Mohr", "Pascal Kopp"),
    ("Christian Munz", "Lubka Röger"),
    ("Ute Schorpp", "Lubka Röger"),
    ("Teamleiterin Kundenberatung", "Immobilienberaterin"),
    ("Gebietsleiterin Immobilienverkauf", "Immobilienberaterin"),
    ("Gebietsleiter Immobilienverkauf", "Immobilienberater"),
    ("Leitung Immobilienverkauf", "Inhaber &amp; Sachverständiger"),
    ("Leitung Immobilienvermittlung", "Inhaber &amp; Sachverständiger"),
    ("Leiter Immobilienverkauf", "Inhaber &amp; Sachverständiger"),
    ("streit_facepile.jpg", "oberholz_facepile.jpg"),
    ("streit_facepile_1.jpg", "oberholz_facepile.jpg"),
    ("/media/team/team_schorpp.jpg", "/media/team/lubka-roeger.jpg"),
    (r"\/media\/team\/team_schorpp.jpg", r"\/media\/team\/lubka-roeger.jpg"),
)


def needs_work(text: str) -> bool:
    if "Service-PIN" in text or "EE36AKY" in text:
        return True
    # common PIN prefix after EE
    if "Service-PIN" in text:
        return True
    for old, _ in REPLACEMENTS:
        if old in text:
            return True
    if "Lubka Röger - Immobilienberater" in text:
        return True
    return False


def patch(text: str) -> tuple[str, int, int]:
    pin_n = 0
    text2, n = PIN_RE.subn("", text)
    pin_n += n
    text = text2
    if "Service-PIN" in text:
        text2, n = PIN_SPAN_RE.subn("", text)
        pin_n += n
        text = text2
    name_n = 0
    for old, new in REPLACEMENTS:
        if old in text:
            c = text.count(old)
            text = text.replace(old, new)
            name_n += c
    text = text.replace(
        "Lubka Röger - Immobilienberater",
        "Lubka Röger - Immobilienberaterin",
    )
    return text, pin_n, name_n


def main() -> None:
    # Prefer regionen second-level html + public roots; avoid huge rescans of already-clean if possible
    files: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if any(x in SKIP for x in p.parts):
            continue
        files.append(p)
    print("html", len(files), flush=True)

    changed = pin_total = name_total = skipped = 0
    for i, path in enumerate(files, 1):
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        # Quick byte filter before decode
        if b"Service-PIN" not in raw and b"Ute Schorpp" not in raw and b"Kersten Streit" not in raw and b"Wolfgang Mayer" not in raw and b"Axel Winkler" not in raw and b"team_schorpp" not in raw and b"streit_facepile" not in raw and b"Christian Munz" not in raw and b"Ren" not in raw:
            skipped += 1
            if i % 3000 == 0:
                print(f"progress {i}/{len(files)} changed {changed} skipped {skipped}", flush=True)
            continue
        text = raw.decode("utf-8", errors="replace")
        if not needs_work(text):
            skipped += 1
            continue
        new_text, pin_n, name_n = patch(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            pin_total += pin_n
            name_total += name_n
        if i % 2000 == 0:
            print(f"progress {i}/{len(files)} changed {changed} pins {pin_total} names {name_total}", flush=True)

    print("done changed", changed, "pins", pin_total, "names", name_total, "skipped", skipped, flush=True)

    # verify felde + index
    for rel in [
        "index.html",
        "public/regionen/felde/immobilienmakler.html",
        "public/regionen/felde/immobilie-verkaufen.html",
    ]:
        p = ROOT / rel
        t = p.read_text(encoding="utf-8", errors="replace")
        print(
            "verify",
            rel,
            "PIN",
            ("Service-PIN" in t),
            "Ute",
            ("Ute Schorpp" in t),
            "Penn+t7a7913",
            ("t7a7913_1.png" in t and "Michael Penn" in t),
            flush=True,
        )


if __name__ == "__main__":
    main()
