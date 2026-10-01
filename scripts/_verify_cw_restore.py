#!/usr/bin/env python3
from pathlib import Path

t = Path("index.html").read_text(encoding="utf-8")
checks = {
    "contact-widget.html": "contact-widget.html" in t,
    "cw-local-overlay": "cw-local-overlay" in t,
    "Lokale Ansicht": "Lokale Ansicht" in t,
    "override.js": "oberholz-contact-override" in t,
    "contact-widget.css": "oberholz-contact-widget.css" in t,
    "Promise.resolve stub": "Promise.resolve({ text:" in t,
}
for k, v in checks.items():
    print(k, v)
needle = "fetch('/theme/contact-widget.html')"
i = t.find(needle)
print("fetch idx", i)
if i >= 0:
    print(t[i - 60 : i + 80])
