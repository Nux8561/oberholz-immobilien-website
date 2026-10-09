#!/usr/bin/env python3
"""Remove the regio-goodie 'Marktgerechte Bewertung / Energieausweis' promo block."""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SECTION_RE = re.compile(
    r'<section\b[^>]*>\s*'
    r'<div class="container">\s*'
    r'<div class="regio-goodie\b[\s\S]*?</div>\s*'
    r'</div>\s*'
    r'</section>',
    re.I,
)

# Fallback: unmatched nesting – cut from section start containing the div
FALLBACK_MARKER = 'class="regio-goodie'


def strip_section(html: str) -> str:
    updated, n = SECTION_RE.subn("", html)
    if n:
        return updated

    idx = html.find(FALLBACK_MARKER)
    while idx >= 0:
        start = html.rfind("<section", 0, idx)
        if start < 0:
            break
        end = html.find("</section>", idx)
        if end < 0:
            break
        end += len("</section>")
        html = html[:start] + html[end:]
        idx = html.find(FALLBACK_MARKER)
    return html


def stub_energieausweis() -> None:
    path = ROOT / "public" / "leistungen" / "energieausweis-kostenlos.html"
    stub = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex, follow"/>
<link rel="canonical" href="/leistungen.html"/>
<title>Leistung nicht verfügbar | Oberholz Immobilien</title>
<meta name="description" content="Diese Leistung bieten wir derzeit nicht an."/>
<style>
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f9;color:#1b2430}
  main{max-width:40rem;margin:12vh auto;padding:2rem;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:.75rem}
  h1{font-size:1.5rem;margin:0 0 .75rem}
  p{line-height:1.55;margin:0 0 1.25rem}
  a{color:#223a66;font-weight:600}
</style>
</head>
<body>
<main>
  <h1>Diese Leistung bieten wir nicht an</h1>
  <p>Den kostenlosen Energieausweis und die marktgerechte Bewertung als eigenständige Leistung bieten wir nicht an. Bitte nutzen Sie unsere aktuellen Leistungen.</p>
  <p><a href="/leistungen.html">Zur Leistungsübersicht</a> · <a href="/">Zur Startseite</a></p>
</main>
</body>
</html>
"""
    path.write_text(stub, encoding="utf-8")


def main() -> None:
    started = time.time()
    stub_energieausweis()
    seen = changed = 0
    paths = [ROOT / "index.html"]
    for dirpath, _d, files in os.walk(ROOT / "public"):
        for name in files:
            if name.lower().endswith(".html"):
                paths.append(Path(dirpath) / name)

    for path in paths:
        seen += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if FALLBACK_MARKER not in text and "regio-goodie" not in text:
            continue
        # Skip pure CSS-only mentions? Still strip sections; CSS rules can stay harmlessly
        if FALLBACK_MARKER not in text:
            continue
        updated = strip_section(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print("removed", path, flush=True)
    print(
        "DONE",
        {"seen": seen, "changed": changed},
        f"elapsed={time.time()-started:.0f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
