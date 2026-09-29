# -*- coding: utf-8 -*-
"""Standort-Nav Fix ohne Regex-Backtracking – nur exakte Blocks + Href-Maps."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]

CITIES = [
    ("muenster", "Münster"),
    ("essen", "Essen"),
    ("bochum", "Bochum"),
]


def desktop_block(space: bool) -> str:
    sp = " " if space else ""
    parts = []
    for slug, name in CITIES:
        parts.append(
            f'<a class="dropdown-item{sp}" href="/kontakt/immobilienmakler-{slug}.html" '
            f'title="Immobilienmakler {name}"> '
            f'<span class="menu-label">Immobilienmakler {name}</span></a>'
        )
    return "".join(parts) + '</div><div class="col-12 col-md-6">'


def old_desktop_block(space: bool) -> str:
    sp = " " if space else ""
    # Exact mirrored IE block (two columns)
    col1 = [
        ("hamburg", "Hamburg"),
        ("duesseldorf", "Düsseldorf"),
        ("hannover", "Hannover"),
    ]
    col2 = [
        ("stuttgart", "Stuttgart"),
        ("villingen-schwenningen", "Villingen-Schwenningen"),
        ("frankfurt-am-main", "Frankfurt am Main"),
        ("muenchen", "München"),
    ]

    def link(slug: str, name: str) -> str:
        return (
            f'<a class="dropdown-item{sp}" href="/kontakt/immobilienmakler-{slug}.html" '
            f'title="Immobilienmakler {name}"> '
            f'<span class="menu-label">Immobilienmakler {name}</span></a>'
        )

    return (
        "".join(link(s, n) for s, n in col1)
        + '</div><div class="col-12 col-md-6">'
        + "".join(link(s, n) for s, n in col2)
    )


def old_mobile_block() -> str:
    cities = [
        ("hamburg", "Hamburg"),
        ("duesseldorf", "Düsseldorf"),
        ("hannover", "Hannover"),
        ("stuttgart", "Stuttgart"),
        ("villingen-schwenningen", "Villingen-Schwenningen"),
        ("frankfurt-am-main", "Frankfurt am Main"),
        ("muenchen", "München"),
    ]
    return "".join(
        f'<li class="my-3 "><a class="" href="/kontakt/immobilienmakler-{slug}.html" '
        f'title="Immobilienmakler {name}">Immobilienmakler {name}</a></li>'
        for slug, name in cities
    )


def new_mobile_block() -> str:
    return "".join(
        f'<li class="my-3 "><a class="" href="/kontakt/immobilienmakler-{slug}.html" '
        f'title="Immobilienmakler {name}">Immobilienmakler {name}</a></li>'
        for slug, name in CITIES
    )


HREF_MAP = [
    ("/kontakt/immobilienmakler-hamburg.html", "/kontakt/immobilienmakler-muenster.html"),
    ("/kontakt/immobilienmakler-duesseldorf.html", "/kontakt/immobilienmakler-essen.html"),
    ("/kontakt/immobilienmakler-hannover.html", "/kontakt/immobilienmakler-bochum.html"),
    ("/kontakt/immobilienmakler-stuttgart.html", "/kontakt/immobilienmakler-muenster.html"),
    ("/kontakt/immobilienmakler-villingen-schwenningen.html", "/kontakt/immobilienmakler-essen.html"),
    ("/kontakt/immobilienmakler-frankfurt-am-main.html", "/kontakt/immobilienmakler-bochum.html"),
    ("/kontakt/immobilienmakler-muenchen.html", "/kontakt/immobilienmakler-muenster.html"),
]

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
        "bundesweit und auch regional vor Ort in Ihrer Nähe.",
        "persönlich vor Ort in Münster, Essen und Bochum.",
    ),
]

NEEDLES = [
    b"immobilienmakler-hamburg.html",
    b"immobilienmakler-stuttgart.html",
    b"immobilienmakler-muenchen.html",
    b"immobilienmakler-duesseldorf.html",
    b"immobilienmakler-hannover.html",
    b"immobilienmakler-frankfurt",
    b"immobilienmakler-villingen",
    b"Immobilienmakler Stuttgart",
    b"Immobilienmakler Hamburg",
    b"bundesweit und auch regional",
]

SKIP_DIRS = {"media", "mediatypes", "theme", "assets", ".git", "node_modules"}

OLD_DESKTOP_SP = old_desktop_block(True)
OLD_DESKTOP_NOSP = old_desktop_block(False)
NEW_DESKTOP_SP = desktop_block(True)
NEW_DESKTOP_NOSP = desktop_block(False)
OLD_MOBILE = old_mobile_block()
NEW_MOBILE = new_mobile_block()


def patch_text(text: str) -> tuple[str, int]:
    n = 0
    if OLD_DESKTOP_SP in text:
        text = text.replace(OLD_DESKTOP_SP, NEW_DESKTOP_SP)
        n += 1
    if OLD_DESKTOP_NOSP in text:
        text = text.replace(OLD_DESKTOP_NOSP, NEW_DESKTOP_NOSP)
        n += 1
    if OLD_MOBILE in text:
        text = text.replace(OLD_MOBILE, NEW_MOBILE)
        n += 1
    for old, new in HREF_MAP:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    for old, new in LABEL_MAP:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    for old, new in TEXT_FIXES:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    return text, n


def main() -> None:
    # verify blocks look right
    print("old desktop sp len", len(OLD_DESKTOP_SP))
    print("new desktop sp len", len(NEW_DESKTOP_SP))
    print("old mobile len", len(OLD_MOBILE))

    start = time.time()
    checked = scanned = changed = errors = 0
    ops = 0

    targets = [ROOT / "public", ROOT]
    seen = set()

    for base in targets:
        if not base.exists():
            continue
        walker = os.walk(base) if base.name == "public" or base == ROOT / "public" else None
        if base == ROOT:
            # only root html files
            for name in os.listdir(base):
                if name.endswith(".html"):
                    path = base / name
                    key = str(path.resolve())
                    if key in seen:
                        continue
                    seen.add(key)
                    checked += 1
                    try:
                        raw = path.read_bytes()
                    except OSError:
                        errors += 1
                        continue
                    if not any(n in raw for n in NEEDLES):
                        continue
                    scanned += 1
                    text = raw.decode("utf-8", errors="ignore")
                    new_text, n = patch_text(text)
                    if n and new_text != text:
                        try:
                            path.write_text(new_text, encoding="utf-8")
                            changed += 1
                            ops += n
                            print("patched", path.name, "ops", n, flush=True)
                        except OSError:
                            errors += 1
            continue

        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if not name.endswith(".html"):
                    continue
                path = Path(root) / name
                key = str(path.resolve())
                if key in seen:
                    continue
                seen.add(key)
                checked += 1
                try:
                    raw = path.read_bytes()
                except OSError:
                    errors += 1
                    continue
                if not any(n in raw for n in NEEDLES):
                    if checked % 3000 == 0:
                        print(
                            f"... checked {checked} scanned {scanned} changed {changed} ({time.time()-start:.0f}s)",
                            flush=True,
                        )
                    continue
                scanned += 1
                text = raw.decode("utf-8", errors="ignore")
                new_text, n = patch_text(text)
                if n and new_text != text:
                    try:
                        path.write_text(new_text, encoding="utf-8")
                        changed += 1
                        ops += n
                    except OSError:
                        errors += 1
                if scanned % 300 == 0:
                    print(
                        f"... checked {checked} scanned {scanned} changed {changed} ops {ops} ({time.time()-start:.0f}s)",
                        flush=True,
                    )

    print(
        "DONE checked",
        checked,
        "scanned",
        scanned,
        "changed",
        changed,
        "ops",
        ops,
        "errors",
        errors,
        f"elapsed {time.time()-start:.1f}s",
    )


if __name__ == "__main__":
    main()
