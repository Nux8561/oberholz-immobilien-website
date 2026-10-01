#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("public/theme/contact-widget.html").read_text(encoding="utf-8")
print("tels:")
for m in re.finditer(r'tel:[^"\']+', t):
    print(" ", m.group(0))

i = t.find("Support-Hotline")
print("\nSUPPORT BLOCK:\n", t[i - 250 : i + 400])

# leftover EE markers
for bad in ["0711", "14.700", "dena", "BAFA", "20 Jahre", "Immobilien Experten", "ee-experten"]:
    print("left", bad, t.count(bad))
