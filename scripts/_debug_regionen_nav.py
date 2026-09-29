# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

samples = [
    "public/regionen/weilburg/immobilie-verkaufen.html",
    "public/regionen/havelsee.html",
    "public/regionen/siebenbaeumen/immobilienmakler.html",
]

sys.path.insert(0, "scripts")
from fix_standorte_fast import patch_html_text, DESKTOP_CITY_RE2, MOBILE_CITY_RE, HREF_MAP

for rel in samples:
    p = Path(rel)
    if not p.exists():
        print("missing", rel)
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    print("====", rel, "len", len(t))
    for needle in [
        "immobilienmakler-hamburg.html",
        "/kontakt/immobilienmakler-hamburg.html",
        "Immobilienmakler Hamburg",
        "Immobilienmakler Stuttgart",
        "dropdown-item",
    ]:
        print(f"  count {needle!r}: {t.count(needle)}")

    # show hamburg contexts
    i = t.find("immobilienmakler-hamburg")
    if i >= 0:
        print("  ctx:", re.sub(r"\s+", " ", t[max(0, i - 80) : i + 120]))

    m = DESKTOP_CITY_RE2.search(t)
    print("  desktop_re", bool(m), "len", len(m.group(0)) if m else 0)
    m2 = MOBILE_CITY_RE.search(t)
    print("  mobile_re", bool(m2), "len", len(m2.group(0)) if m2 else 0)

    new, stats = patch_html_text(t)
    print("  stats", stats, "changed", new != t)
    # manual href test
    for old in HREF_MAP:
        if old in t:
            print("  has href", old)
