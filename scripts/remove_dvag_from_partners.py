#!/usr/bin/env python3
"""Remove DVAG only from .partner-logos strips; keep footer/header coop."""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DVAG_IN_PARTNERS = re.compile(
    r'(<div\b[^>]*\bpartner-logos\b[^>]*>)([\s\S]*?)(</div>)',
    re.I,
)

DVAG_ANCHOR = re.compile(
    r'<a\b[^>]*>\s*<img\b[^>]*\bsrc="/media/dvag-logo\.svg"[^>]*/?>\s*</a>\s*',
    re.I,
)

DVAG_IMG = re.compile(
    r'<img\b[^>]*\bsrc="/media/dvag-logo\.svg"[^>]*/?>\s*',
    re.I,
)


def strip_dvag_in_partner_block(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        inner = DVAG_ANCHOR.sub("", m.group(2))
        inner = DVAG_IMG.sub("", inner)
        return m.group(1) + inner + m.group(3)

    return DVAG_IN_PARTNERS.sub(repl, html)


def main() -> None:
    changed = 0
    paths = [ROOT / "index.html"]
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)

    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "partner-logos" not in text or "dvag-logo.svg" not in text:
            continue
        updated = strip_dvag_in_partner_block(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print("changed", path)
    print("DONE changed=", changed)


if __name__ == "__main__":
    main()
