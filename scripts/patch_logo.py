"""Patch IE logos on the homepage. Prefer scripts/rebrand_oberholz.py for all pages."""

from pathlib import Path

# Kept for one-off homepage logo swaps. Site-wide branding:
#   python scripts/rebrand_oberholz.py

path = Path("index.html")
text = path.read_text(encoding="utf-8")
replacements = (
    (
        'alt="Logo Immobilien Experten" class="d-block d-md-none" fetchpriority="high" height="54" src="/media/ie_logo.svg" width="200"',
        'alt="Oberholz Immobilien" class="d-block d-md-none" fetchpriority="high" height="92" src="/media/oberholz-logo.png" width="200"',
    ),
    (
        'alt="Logo Immobilien Experten" class="d-none d-md-block" fetchpriority="high" height="54" src="/media/ie_logo.svg" width="200"',
        'alt="Oberholz Immobilien" class="d-none d-md-block" fetchpriority="high" height="92" src="/media/oberholz-logo.png" width="200"',
    ),
    (
        'alt="Logo Immobilien Experten" class="img-fluid" loading="lazy" src="/media/ie_logo.svg" width="200"',
        'alt="Oberholz Immobilien" class="img-fluid" loading="lazy" src="/media/oberholz-logo.png" width="200"',
    ),
    (
        'alt="Logo Immobilien Experten" class="img-fluid" src="/media/ie_logo.svg" width="300"',
        'alt="Oberholz Immobilien" class="img-fluid" src="/media/oberholz-logo.png" width="300"',
    ),
)
for old, new in replacements:
    text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("ie_logo left", text.count("ie_logo.svg"))
print("oberholz-logo", text.count("oberholz-logo.png"))
