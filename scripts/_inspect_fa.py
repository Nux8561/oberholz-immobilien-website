#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("index.html").read_text(encoding="utf-8")
print("fa-brands count", t.count("fa-brands"))
print("fab count", t.count("fab "))
for m in re.finditer(r'href="([^"]*(?:font-?awesome|fa-brands|all\.min|brands)[^"]*)"', t, re.I):
    print("css", m.group(1))
for m in re.finditer(r'class="([^"]*fa[^"]*)"', t):
    c = m.group(1)
    if "fa-" in c or c.startswith("fa "):
        if "fa-envelope" in c or "fa-brands" in c or "fa-linkedin" in c or "fa-youtube" in c or "fa-phone" in c:
            print("icon class:", c)
# linkedin block
i = t.find("linkedin.com/company/oberholz")
print("social block:", t[i - 100 : i + 350])
