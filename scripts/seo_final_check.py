# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

FOREIGN_HREF = re.compile(
    r"""href=(["'])(/(?:regionen/(?!bochum|essen|muenster)[^"']*|kontakt/immobilienmakler-(?!bochum|essen|muenster)[^"']*))\1""",
    re.I,
)
MUNSTER_HREF = re.compile(r"""/regionen/munster(?:/|"|'|\?|#|$)""", re.I)
BIZ_PHRASES = [
    "Immobilienmakler München",
    "Immobilienmakler Munchen",
    "Immobilienmakler Hamburg",
    "Immobilienmakler Düsseldorf",
    "Immobilienmakler Duesseldorf",
    "Immobilienmakler Frankfurt",
    "Immobilienmakler Stuttgart",
    "Immobilienmakler Hannover",
]


def main() -> None:
    issues = []
    files = [ROOT / "index.html"] + list(PUBLIC.rglob("*.html"))
    munster_links = 0
    foreign_hrefs = 0
    biz_hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for m in FOREIGN_HREF.finditer(text):
            foreign_hrefs += 1
            if len(issues) < 30:
                issues.append(f"foreign_href {rel} {m.group(2)}")
        for m in MUNSTER_HREF.finditer(text):
            munster_links += 1
            if len(issues) < 40:
                issues.append(f"noncanonical_munster {rel} {m.group(0)}")
        if "/immobilien/" in rel:
            continue
        for phrase in BIZ_PHRASES:
            if phrase in text:
                biz_hits.append(f"{rel}: {phrase}")
                break

    # sitemap
    sitemap_hits = []
    for sp in (ROOT / "analysis").glob("sitemap*"):
        t = sp.read_text(encoding="utf-8", errors="replace")
        if "/regionen/" in t and "muenchen" in t.lower():
            sitemap_hits.append(str(sp))

    print("foreign_hrefs", foreign_hrefs)
    print("noncanonical_munster_links", munster_links)
    print("biz_phrase_pages", len(biz_hits))
    for x in biz_hits[:20]:
        print(" BIZ", x)
    print("sitemap_foreign", sitemap_hits)
    print("region_dirs", sorted(p.name for p in (PUBLIC / "regionen").iterdir() if p.is_dir()))
    print("issues_sample")
    for i in issues[:25]:
        print(" ", i)


if __name__ == "__main__":
    main()
