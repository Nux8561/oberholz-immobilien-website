#!/usr/bin/env python3
from pathlib import Path
import re

html = Path("scripts/_cw_original_widget.html").read_text(encoding="utf-8")

# Contact-related snippets
for pat in [
    r'tel:\+?[0-9]+',
    r'mailto:[^"\'>\s]+',
    r'0800[^<"\']{0,40}',
    r'wa\.me/[0-9]+',
    r'media/[^"\']+\.(?:jpg|png|webp)',
    r'Immobilien Experten',
    r'Kersten Streit',
    r'info@immobilien-experten\.de',
]:
    found = sorted(set(re.findall(pat, html)))
    print("===", pat)
    for f in found[:20]:
        print(" ", f)

# Oberholz contacts from index
idx = Path("index.html").read_text(encoding="utf-8")
for pat in [r'tel:\+?[0-9]+', r'mailto:[^"\'>\s]+', r'0251[^<"\']{0,30}', r'mail@[^"\'>\s]+']:
    found = sorted(set(re.findall(pat, idx)))
    print("INDEX", pat, found[:10])
