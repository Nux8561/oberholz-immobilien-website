from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
detail = (ROOT / "public/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html").read_text(encoding="utf-8", errors="replace")

# Extract <main>...</main>
m = re.search(r"<main>(.*?)</main>", detail, re.S | re.I)
print("main found", bool(m), "len", len(m.group(1)) if m else 0)
if m:
    main = m.group(1)
    (ROOT / "assets/oberholz/_sample_main.html").write_text(main, encoding="utf-8")
    # find key text snippets
    texts = re.findall(r">([^<]{20,120})<", main)
    for t in texts[:40]:
        t = t.strip()
        if t:
            print("-", t[:120])
