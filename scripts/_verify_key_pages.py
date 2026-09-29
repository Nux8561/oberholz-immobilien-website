from pathlib import Path
import re

ROOT = Path(".")
for rel in [
    "index.html",
    "public/regionen/felde/immobilienmakler.html",
    "public/regionen/felde/immobilie-verkaufen.html",
]:
    p = ROOT / rel
    t = p.read_text(encoding="utf-8", errors="replace")
    print("===", rel)
    print(" PIN", "Service-PIN" in t)
    print(" Ute", "Ute Schorpp" in t)
    print(" team_schorpp", "team_schorpp" in t)
    print(" Lubka", "Lubka" in t)
    for m in re.finditer(r"<img[^>]+>", t):
        tag = m.group(0)
        if not any(k in tag for k in ("bannerright", "facepile", "/media/team/")):
            continue
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if not src:
            continue
        s = src.group(1)
        if any(x in s for x in ("t7a", "facepile", "team/")):
            a = (alt.group(1) if alt else "")[:70]
            print(" ", s.split("/")[-1], "|", a)
