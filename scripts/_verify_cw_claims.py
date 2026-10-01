#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("public/theme/contact-widget.html").read_text(encoding="utf-8")

# Check encoding of replacements
for needle in ["Persönlich vor Ort", "DIN-zertifizierter Gutachter", "Bochum &amp; Münster", "Bochum & Münster", "0251 28 42 90 90"]:
    print(repr(needle), t.count(needle))

# Show all badge plain texts
for m in re.finditer(r'class="cw-badge[^"]*"[^>]*>([\s\S]*?)</span>', t):
    plain = re.sub(r"<[^>]+>", "", m.group(1))
    plain = re.sub(r"\s+", " ", plain).strip()
    if plain:
        print("BADGE:", plain)

i = t.find("Support-Hotline")
print("HOTLINE SNIP:", t[i : i + 220] if i >= 0 else "none")

# any mojibake?
for bad in ["Persnlich", "Mnster", "Ã", "�"]:
    if bad in t:
        print("MOJIBAKE?", bad, t.count(bad))
