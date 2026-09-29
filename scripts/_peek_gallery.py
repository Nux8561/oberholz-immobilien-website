from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
main = (ROOT / "assets/oberholz/_sample_main.html")
if not main.exists():
    detail = (ROOT / "public/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<main>(.*?)</main>", detail, re.S | re.I)
    main.write_text(m.group(1), encoding="utf-8")
text = main.read_text(encoding="utf-8")
print("main len", len(text))

# Find gallery / carousel blocks
for pat in ["carousel", "swiper", "gallery", "object-zoom", "data-bs-slide", "thumb"]:
    print(pat, text.lower().count(pat.lower()))

# Extract first 8000 chars of visual gallery area (after h1)
h1 = text.find("<h1")
print("around h1:\n", text[h1:h1+2500][:2500])
