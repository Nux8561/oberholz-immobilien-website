#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LINKEDIN = "https://www.linkedin.com/company/oberholz-immobilien"


def patch(html: str) -> str:
    html = html.replace("https://www.youtube.com/@jonaspischner", LINKEDIN)
    html = html.replace('src="/media/play.svg"', 'src="/media/linkedin.svg"')
    html = html.replace('alt="YouTube-Logo Oberholz Immobilien"', 'alt="LinkedIn Oberholz Immobilien"')
    html = html.replace("Oberholz Immobilien YouTube-Channel", "Oberholz Immobilien auf LinkedIn")
    html = html.replace("YouTube-Channel", "LinkedIn-Profil")
    html = re.sub(
        r"Besuchen Sie unseren\s*<a([^>]*)>\s*Oberholz Immobilien auf LinkedIn\s*</a>",
        r'Folgen Sie uns auf <a\1>LinkedIn</a>',
        html,
        flags=re.I,
    )
    return html


changed = 0
for folder in ["public/immobilien"]:
    root = ROOT / folder
    if not root.exists():
        continue
    for path in root.rglob("*.html"):
        data = path.read_bytes()
        if b"jonaspischner" not in data and b"play.svg" not in data:
            continue
        original = data.decode("utf-8", errors="replace")
        html = patch(original)
        if html != original:
            path.write_text(html, encoding="utf-8")
            changed += 1
print(f"Done. Changed {changed}")
