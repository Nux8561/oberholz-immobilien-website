#!/usr/bin/env python3
from pathlib import Path
import re

t = Path("index.html").read_text(encoding="utf-8")
links = re.findall(r'(?:href|src)="(/theme/[^"]+)"', t)
print("theme links:", links)

# ensure css + override present
css = '<link rel="stylesheet" href="/theme/oberholz-contact-widget.css"/>'
js = '<script src="/theme/oberholz-contact-override.js" defer></script>'
changed = False
if "oberholz-contact-widget.css" not in t:
    t = t.replace("</head>", css + "\n</head>", 1)
    changed = True
if "oberholz-contact-override.js" not in t:
    t = t.replace("</body>", js + "\n</body>", 1)
    changed = True
if changed:
    Path("index.html").write_text(t, encoding="utf-8")
    print("index patched with css/js")
else:
    print("index already had assets")
