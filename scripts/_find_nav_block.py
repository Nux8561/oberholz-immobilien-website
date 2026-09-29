# -*- coding: utf-8 -*-
"""Find exact reusable Kontakt city-link blocks across a few sample files."""
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OLD_START = '<a class="dropdown-item " href="/kontakt/immobilienmakler-hamburg.html"'
OLD_ALT = 'href="/kontakt/immobilienmakler-hamburg.html" title="Immobilienmakler Hamburg"'

samples = [
    Path("index.html"),
    Path("public/kontakt/kontakt-aufnehmen.html"),
    Path("public/ueber-uns.html"),
    Path("public/leistungen.html"),
]

for p in samples:
    if not p.exists():
        print("missing", p)
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    n = t.count("immobilienmakler-hamburg.html")
    n2 = t.count("immobilienmakler-stuttgart.html")
    print(f"\n{p}: hamburg={n} stuttgart={n2}")
    # extract first desktop nav city block (from hamburg to muenchen inclusive)
    i = t.find(OLD_START)
    if i < 0:
        i = t.find(OLD_ALT)
        # go back to <a
        i = t.rfind("<a ", max(0, i - 50), i + 1) if i >= 0 else -1
    if i < 0:
        print("  no desktop start")
        continue
    j = t.find("Immobilienmakler München</span></a>", i)
    if j < 0:
        j = t.find("Immobilienmakler M&uuml;nchen</span></a>", i)
    if j < 0:
        print("  no end")
        continue
    j = j + len("Immobilienmakler München</span></a>")
    block = t[i:j]
    print("  block len", len(block))
    Path("scripts/_tmp_old_nav_block.html").write_text(block, encoding="utf-8")
    print("  block head:", block[:120].replace("\n", " "))
    print("  block tail:", block[-120:].replace("\n", " "))

# Check mobile menu pattern
t = Path("public/kontakt/kontakt-aufnehmen.html").read_text(encoding="utf-8", errors="ignore")
for pat in [
    r'data-bs-parent="#Kontakt"[^>]*>.*?</div>\s*</div>',
    r'id="Kontakt"[^>]*>.*?immobilienmakler-muenchen\.html.*?</a>',
]:
    m = re.search(pat, t, re.S)
    print("mobile pat", pat[:40], "found", bool(m), "len", len(m.group(0)) if m else 0)

# Find accordion Kontakt
for marker in ['id="Kontakt"', "data-bs-target=\"#Kontakt\"", ">Kontakt</button>", "Mobilmakler"]:
    print(marker, t.find(marker))
