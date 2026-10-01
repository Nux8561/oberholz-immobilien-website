#!/usr/bin/env python3
from pathlib import Path

p = Path("public/theme/contact-widget.html")
t = p.read_text(encoding="utf-8")
needle = "const closeBtn = document.getElementById('cw-close-btn');"
if "closeBtn.addEventListener" in t:
    print("already patched")
elif needle not in t:
    print("needle missing")
else:
    inject = (
        needle
        + " closeBtn && closeBtn.addEventListener('click', function(e){"
        + " e.preventDefault(); e.stopPropagation(); cwClose(); });"
    )
    t = t.replace(needle, inject, 1)
    p.write_text(t, encoding="utf-8")
    print("patched closeBtn listener")
