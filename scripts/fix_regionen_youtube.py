#!/usr/bin/env python3
from pathlib import Path
import re

LINKEDIN = "https://www.linkedin.com/company/oberholz-immobilien"
SOCIAL = (
    '<div class="mt-4 d-flex align-items-center gap-2">'
    f'<a href="{LINKEDIN}" rel="noopener noreferrer" target="_blank" '
    'aria-label="Oberholz Immobilien auf LinkedIn" title="Oberholz Immobilien auf LinkedIn">'
    '<img alt="LinkedIn" height="28" loading="lazy" src="/media/linkedin.svg" '
    'style="width:28px;height:28px;display:block;" width="28"/></a>'
    f'<a class="text-decoration-none" href="{LINKEDIN}" rel="noopener noreferrer" target="_blank">LinkedIn</a>'
    "</div>"
)
PAT = re.compile(
    r'<div[^>]*(?:mt-5|class="mt-5")[^>]*>\s*'
    r'<a[^>]*href="https://www\.linkedin\.com/company/oberholz-immobilien"[^>]*>\s*'
    r'<img[^>]*linkedin\.svg[^>]*/?>\s*</a>\s*'
    r"<p[^>]*>.*?</p>\s*</div>",
    re.I | re.S,
)

changed = 0
for path in Path("public/regionen").rglob("*.html"):
    data = path.read_bytes()
    if b"jonaspischner" not in data and b"play.svg" not in data:
        continue
    text = data.decode("utf-8", errors="replace")
    html = text.replace("https://www.youtube.com/@jonaspischner", LINKEDIN)
    html = html.replace('src="/media/play.svg"', 'src="/media/linkedin.svg"')
    html = html.replace('alt="YouTube-Logo Oberholz Immobilien"', 'alt="LinkedIn"')
    html = html.replace("Oberholz Immobilien YouTube-Channel", "Oberholz Immobilien auf LinkedIn")
    html = html.replace("YouTube-Channel", "LinkedIn-Profil")
    html = PAT.sub(SOCIAL, html)
    if html != text:
        path.write_text(html, encoding="utf-8")
        changed += 1
print(f"changed {changed}")
