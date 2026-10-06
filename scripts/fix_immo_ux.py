# -*- coding: utf-8 -*-
"""
1) Homepage CTA -> /immobilien.html
2) Add data-container-collapse to long object text blocks
3) Ensure brochures from Desktop RemoveBG PNGs
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
DESK = Path(
    r"C:\Users\lsper\OneDrive - Dominik Scherwinsky\Desktop\Gründungszuschuss"
)
CONTENTIMG = ROOT / "public" / "media" / "contentimg"

SCOUT_CTA_RE = re.compile(
    r"""(<a\b[^>]*\bhref=["'])https://portal\.immobilienscout24\.de/ergebnisliste/82828525(["'][^>]*>\s*Alle aktuellen Immobilien ansehen\s*</a>)""",
    re.I,
)

# Wrap text sections that currently dump full content
SECTION_RE = re.compile(
    r"""(<div class="mb-4">\s*<h2 class="h4 title-color mb-3">(Objektbeschreibung|Ausstattung|Lage)</h2>)([\s\S]*?)(</div>\s*(?=<div class="mb-4">|<div class="[^"]*immo|</div>\s*</div>\s*<div class="col))""",
    re.I,
)


def copy_brochures() -> None:
    CONTENTIMG.mkdir(parents=True, exist_ok=True)
    for name in (
        "brochure_immobilienvermittlung.png",
        "brochure_energieberatung.png",
    ):
        src = DESK / name
        dst = CONTENTIMG / name
        if not src.exists():
            print("MISSING desktop brochure", src, flush=True)
            continue
        shutil.copy2(src, dst)
        # also sync dist if present
        dist = ROOT / "dist" / "media" / "contentimg" / name
        if dist.parent.exists():
            shutil.copy2(src, dist)
        print("copied", name, "-> contentimg", flush=True)


def fix_homepage_cta() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8", errors="replace")
    new, n = SCOUT_CTA_RE.subn(
        r'\1/immobilien.html\2',
        text,
    )
    # also neutralize other identical scout CTAs that open listing
    new2, n2 = re.subn(
        r"""href=["']https://portal\.immobilienscout24\.de/ergebnisliste/82828525["']([^>]*)>(\s*Alle aktuellen Immobilien ansehen\s*)</a>""",
        r'href="/immobilien.html"\1>\2</a>',
        new,
        flags=re.I,
    )
    # update title attr if present
    new2 = new2.replace(
        'title="Alle Immobilien auf Immobilienscout24"',
        'title="Alle aktuellen Immobilien ansehen"',
    )
    if new2 != text:
        path.write_text(new2, encoding="utf-8")
        print("homepage CTA fixed", "scout_re", n, "generic", n2, flush=True)
    else:
        print("homepage CTA unchanged", flush=True)


def add_collapse_attrs(html: str) -> tuple[str, int]:
    ops = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal ops
        head, title, body, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        if "data-container-collapse" in head or "data-container-collapse" in body[:80]:
            return m.group(0)
        # Only collapse longer sections
        if len(re.sub(r"<[^>]+>", "", body)) < 280:
            return m.group(0)
        ops += 1
        return (
            f'<div class="mb-4">'
            f'<h2 class="h4 title-color mb-3">{title}</h2>'
            f'<div data-container-collapse'
            f' data-container-collapse-max-height="220"'
            f' data-container-collapse-more="Mehr anzeigen"'
            f' data-container-collapse-less="Weniger anzeigen"'
            f' data-container-collapse-btn-class="btn btn-link p-0 mt-2">'
            f"{body}"
            f"</div>"
            f"{tail}"
        )

    # simpler approach: find each h2 block
    pattern = re.compile(
        r"""<div class="mb-4">\s*<h2 class="h4 title-color mb-3">(Objektbeschreibung|Ausstattung|Lage)</h2>([\s\S]*?)</div>""",
        re.I,
    )

    def repl2(m: re.Match[str]) -> str:
        nonlocal ops
        title, body = m.group(1), m.group(2)
        if "data-container-collapse" in body:
            return m.group(0)
        plain = re.sub(r"<[^>]+>", "", body)
        if len(plain.strip()) < 280:
            return m.group(0)
        ops += 1
        return (
            f'<div class="mb-4">'
            f'<h2 class="h4 title-color mb-3">{title}</h2>'
            f'<div data-container-collapse'
            f' data-container-collapse-max-height="220"'
            f' data-container-collapse-more="Mehr anzeigen"'
            f' data-container-collapse-less="Weniger anzeigen"'
            f' data-container-collapse-btn-class="container-collapse-toggle-outline">'
            f"{body}"
            f"</div></div>"
        )

    new = pattern.sub(repl2, html)
    return new, ops


def patch_object_pages() -> None:
    changed = ops_total = 0
    for path in (ROOT / "public" / "immobilien").rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "Objektbeschreibung" not in text and "Ausstattung" not in text:
            continue
        new, ops = add_collapse_attrs(text)
        if ops and new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
            ops_total += ops
    print("object pages patched", changed, "sections", ops_total, flush=True)


def main() -> None:
    copy_brochures()
    fix_homepage_cta()
    patch_object_pages()


if __name__ == "__main__":
    main()
