#!/usr/bin/env python3
"""Replace foreign YouTube (@jonaspischner) with Oberholz LinkedIn."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"node_modules", "dist", "dist-regionen", ".git", "analysis", "screenshots", "reference"}

LINKEDIN = "https://www.linkedin.com/company/oberholz-immobilien"

# Core pages first, then any html still containing the old channel
CORE_GLOBS = [
    ROOT / "index.html",
    *(ROOT / "public").glob("*.html"),
    *(ROOT / "public" / "leistungen").glob("*.html"),
    *(ROOT / "public" / "ueber-uns").glob("*.html"),
    *(ROOT / "public" / "service").glob("*.html"),
    *(ROOT / "public" / "ratgeber").glob("*.html"),
    *(ROOT / "public" / "kontakt").glob("*.html"),
    *((ROOT / "public" / "kontakt").glob("*/*.html")),
]


def patch(html: str) -> str:
    html = html.replace("https://www.youtube.com/@jonaspischner", LINKEDIN)
    html = html.replace('src="/media/play.svg"', 'src="/media/linkedin.svg"')
    html = html.replace('alt="YouTube-Logo Oberholz Immobilien"', 'alt="LinkedIn Oberholz Immobilien"')
    html = html.replace("Oberholz Immobilien YouTube-Channel", "Oberholz Immobilien auf LinkedIn")
    html = html.replace("YouTube-Channel", "LinkedIn-Profil")
    # Soften leftover youtube marketing phrases near the social block
    html = re.sub(
        r"Besuchen Sie unseren\s*<a([^>]*)>\s*Oberholz Immobilien auf LinkedIn\s*</a>",
        r'Folgen Sie uns auf <a\1>LinkedIn</a>',
        html,
        flags=re.I,
    )
    return html


def main() -> None:
    files = sorted({p for p in CORE_GLOBS if p.is_file()})
    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8", errors="replace")
        if "jonaspischner" not in original and "play.svg" not in original:
            continue
        html = patch(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"Done. Changed {changed}")


if __name__ == "__main__":
    main()
