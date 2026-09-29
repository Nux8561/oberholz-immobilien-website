# -*- coding: utf-8 -*-
"""
1) Redirect alte IE-Stadt-Unterseiten
2) Patch Nav nur bei echten Alt-Links (präzise Needles)
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import fix_standorte_safe as m  # noqa: E402

# Precise: only real wrong hub links / labels
NEEDLES = [
    b"/kontakt/immobilienmakler-hamburg.html",
    b"/kontakt/immobilienmakler-stuttgart.html",
    b"/kontakt/immobilienmakler-muenchen.html",
    b"/kontakt/immobilienmakler-duesseldorf.html",
    b"/kontakt/immobilienmakler-hannover.html",
    b"/kontakt/immobilienmakler-frankfurt-am-main.html",
    b"/kontakt/immobilienmakler-villingen-schwenningen.html",
    b"Immobilienmakler Stuttgart",
    b"Immobilienmakler Hamburg",
    b"Immobilienmakler M\xc3\xbcnchen",
    b"bundesweit und auch regional",
]

OLD_CITY_DIRS = {
    "immobilienmakler-hamburg": "muenster",
    "immobilienmakler-hannover": "muenster",
    "immobilienmakler-stuttgart": "muenster",
    "immobilienmakler-muenchen": "muenster",
    "immobilienmakler-duesseldorf": "essen",
    "immobilienmakler-villingen-schwenningen": "essen",
    "immobilienmakler-frankfurt-am-main": "bochum",
}

SKIP_DIRS = m.SKIP_DIRS


def redirect_html(target: str) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>Weiterleitung | Oberholz Immobilien</title>\n"
        '<meta name="robots" content="noindex, follow">\n'
        f'<link rel="canonical" href="{target}">\n'
        f'<meta http-equiv="refresh" content="0;url={target}">\n'
        f"<script>location.replace({target!r});</script>\n</head>\n<body>\n"
        f'<p>Weiter zu <a href="{target}">Oberholz Immobilien</a>.</p>\n'
        "</body>\n</html>\n"
    )


def redirect_old_subpages() -> int:
    kontakt = ROOT / "public" / "kontakt"
    n = 0
    for folder, dest in OLD_CITY_DIRS.items():
        d = kontakt / folder
        if not d.is_dir():
            continue
        target = f"/kontakt/immobilienmakler-{dest}.html"
        for path in d.rglob("*.html"):
            path.write_text(redirect_html(target), encoding="utf-8")
            n += 1
        print(f"redirected {n} under {folder} -> {target}")
    return n


def patch_tree() -> None:
    start = time.time()
    checked = scanned = changed = errors = ops_total = 0
    for root, dirs, files in os.walk(ROOT / "public"):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not name.endswith(".html"):
                continue
            path = Path(root) / name
            checked += 1
            try:
                raw = path.read_bytes()
            except OSError:
                errors += 1
                continue
            if not any(n in raw for n in NEEDLES):
                if checked % 4000 == 0:
                    print(
                        f"... checked {checked} scanned {scanned} changed {changed} ({time.time()-start:.0f}s)",
                        flush=True,
                    )
                continue
            scanned += 1
            text = raw.decode("utf-8", errors="ignore")
            new_text, ops = m.patch_text(text)
            if ops and new_text != text:
                try:
                    path.write_text(new_text, encoding="utf-8")
                    changed += 1
                    ops_total += ops
                except OSError:
                    errors += 1
            if scanned % 400 == 0:
                print(
                    f"... checked {checked} scanned {scanned} changed {changed} ops {ops_total} ({time.time()-start:.0f}s)",
                    flush=True,
                )

    # root index
    idx = ROOT / "index.html"
    if idx.exists():
        raw = idx.read_bytes()
        if any(n in raw for n in NEEDLES):
            text = raw.decode("utf-8", errors="ignore")
            new_text, ops = m.patch_text(text)
            if ops and new_text != text:
                idx.write_text(new_text, encoding="utf-8")
                changed += 1
                print("patched index.html")

    print(
        "DONE checked",
        checked,
        "scanned",
        scanned,
        "changed",
        changed,
        "ops",
        ops_total,
        "errors",
        errors,
        f"elapsed {time.time()-start:.1f}s",
    )


def main() -> None:
    print("=== redirect old city subpages ===")
    redirect_old_subpages()
    print("=== patch remaining wrong nav links ===")
    patch_tree()


if __name__ == "__main__":
    main()
