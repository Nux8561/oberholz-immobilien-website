#!/usr/bin/env python3
from pathlib import Path
import re

NEW_ITEMS = (
    '<a class="dropdown-item" href="/leistungen/mehrfamilienhaeuser-kaufen-bochum.html" '
    'title="Mehrfamilienhäuser kaufen in Bochum"> '
    '<span class="menu-label">Mehrfamilienhäuser kaufen</span></a>'
    '<a class="dropdown-item" href="/leistungen/wohnungen-kaufen-bochum.html" '
    'title="Wohnungen kaufen in Bochum"> '
    '<span class="menu-label">Wohnungen kaufen</span></a>'
)

for name in [
    "mehrfamilienhaeuser-kaufen-bochum.html",
    "wohnungen-kaufen-bochum.html",
    "immobilienverkauf.html",
]:
    path = Path("public/leistungen") / name
    text = path.read_text(encoding="utf-8")
    if "mehrfamilienhaeuser-kaufen-bochum.html" in text and 'class="dropdown-item" href="/leistungen/mehrfamilienhaeuser-kaufen-bochum.html"' in text:
        print(name, "already")
        continue
    text2, n = re.subn(
        r'(<a class="dropdown-item" href="/leistungen/immobilienverkauf\.html"[^>]*>.*?</a>)',
        r"\1" + NEW_ITEMS,
        text,
        count=1,
        flags=re.S,
    )
    if not n:
        text2, n = re.subn(
            r'(<a class="dropdown-item" href="/leistungen/immobilienfinanzierung\.html"[^>]*>.*?</a>)',
            NEW_ITEMS + r"\1",
            text,
            count=1,
            flags=re.S,
        )
    if n:
        path.write_text(text2, encoding="utf-8")
        print("patched", name)
    else:
        print("failed", name)
