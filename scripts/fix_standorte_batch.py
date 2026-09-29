# -*- coding: utf-8 -*-
"""Patch remaining wrong city nav + bundesweit copy. Batched dirs for OneDrive."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "scripts"))
from fix_standorte_fast import patch_html_text, CITIES  # noqa: E402

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

DIRS = [
    ROOT,
    ROOT / "public",
    ROOT / "public" / "kontakt",
    ROOT / "public" / "leistungen",
    ROOT / "public" / "service",
    ROOT / "public" / "ueber-uns",
    ROOT / "public" / "ratgeber",
    ROOT / "public" / "immotipp",
    ROOT / "public" / "immobilien",
]


def collect(limit_per_dir: int | None = None) -> list[Path]:
    files: list[Path] = []
    seen = set()
    for d in DIRS:
        if not d.exists():
            continue
        batch = list(d.glob("*.html"))
        if limit_per_dir:
            batch = batch[:limit_per_dir]
        for p in batch:
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                files.append(p)
        # one nested level for leistungen/service etc.
        if d.name in ("leistungen", "service", "ueber-uns", "ratgeber", "kontakt"):
            for sub in d.iterdir():
                if sub.is_dir():
                    for p in sub.glob("*.html"):
                        key = str(p.resolve())
                        if key not in seen:
                            seen.add(key)
                            files.append(p)
    return files


def main() -> None:
    files = collect()
    print("candidates", len(files))
    changed = 0
    scanned = 0
    for path in files:
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if not any(n in raw for n in NEEDLES):
            continue
        scanned += 1
        text = raw.decode("utf-8", errors="ignore")
        new_text, stats = patch_html_text(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print("patched", path.relative_to(ROOT), stats)
    print("DONE scanned", scanned, "changed", changed)

    # Verify kontakt nav/table/bundesweit
    t = (ROOT / "public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")
    print("bundesweit left", t.count("bundesweit und auch regional"))
    print("hamburg href left", t.count("immobilienmakler-hamburg.html"))
    for c in CITIES:
        print(c["slug"], t.count(f"immobilienmakler-{c['slug']}.html"))


if __name__ == "__main__":
    main()
