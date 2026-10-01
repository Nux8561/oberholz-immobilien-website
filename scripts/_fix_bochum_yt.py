#!/usr/bin/env python3
from pathlib import Path

LINKEDIN = "https://www.linkedin.com/company/oberholz-immobilien"
for p in Path("public/regionen/bochum").glob("*.html"):
    t = p.read_text(encoding="utf-8", errors="replace")
    h = (
        t.replace("https://www.youtube.com/@jonaspischner", LINKEDIN)
        .replace('src="/media/play.svg"', 'src="/media/linkedin.svg"')
        .replace('alt="YouTube-Logo Oberholz Immobilien"', 'alt="LinkedIn"')
        .replace("Oberholz Immobilien YouTube-Channel", "Oberholz Immobilien auf LinkedIn")
    )
    if h != t:
        p.write_text(h, encoding="utf-8")
        print("fixed", p.name)
    else:
        print("nochange", p.name)
