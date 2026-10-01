#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOCIAL_BLOCK = (
    '<div class="mt-4 d-flex align-items-center gap-2">'
    '<a href="https://www.linkedin.com/company/oberholz-immobilien" '
    'rel="noopener noreferrer" target="_blank" aria-label="Oberholz Immobilien auf LinkedIn" '
    'title="Oberholz Immobilien auf LinkedIn">'
    '<img alt="LinkedIn" height="28" loading="lazy" src="/media/linkedin.svg" '
    'style="width:28px;height:28px;display:block;" width="28"/>'
    "</a>"
    '<a class="text-decoration-none" href="https://www.linkedin.com/company/oberholz-immobilien" '
    'rel="noopener noreferrer" target="_blank">LinkedIn</a>'
    "</div>"
)

# Match any footer social div that still wraps linkedin.svg + paragraph text
PAT = re.compile(
    r'<div[^>]*(?:mt-5|class="mt-5")[^>]*>\s*'
    r'<a[^>]*href="https://www\.linkedin\.com/company/oberholz-immobilien"[^>]*>\s*'
    r'<img[^>]*linkedin\.svg[^>]*/?>\s*</a>\s*'
    r"<p[^>]*>.*?</p>\s*</div>",
    re.I | re.S,
)

files = [ROOT / "index.html"]
for folder in [
    ROOT / "public",
    ROOT / "public" / "leistungen",
    ROOT / "public" / "ueber-uns",
    ROOT / "public" / "service",
    ROOT / "public" / "ratgeber",
    ROOT / "public" / "kontakt",
]:
    files.extend(folder.glob("*.html"))

changed = 0
left = 0
for path in sorted(set(files)):
    if not path.is_file():
        continue
    original = path.read_text(encoding="utf-8", errors="replace")
    html, n = PAT.subn(SOCIAL_BLOCK, original)
    # also nuke remaining inflated counts if any
    html2 = html.replace("+14.700 zufriedene Kunden", "Persönliche Beratung in Bochum")
    html2 = html2.replace("über 11.000 zufriedene Kunden", "persönliche Beratung vor Ort in Bochum")
    if html2 != original:
        path.write_text(html2, encoding="utf-8")
        changed += 1
        print("updated", path.relative_to(ROOT), "social_subs", n)
    if "Besuchen Sie unseren" in html2 and "linkedin" in html2.lower():
        left += 1
        print("still verbose", path.relative_to(ROOT))

print("changed", changed, "still verbose", left)

# verify counts
for needle in ["14.700", "11.000 zufriedene", "Besuchen Sie unseren"]:
    c = 0
    for path in files:
        if path.is_file() and needle in path.read_text(encoding="utf-8", errors="replace"):
            c += 1
    print(needle, c)
