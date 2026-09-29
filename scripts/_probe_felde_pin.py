from pathlib import Path
import re

felde = Path("public/regionen/felde")
print("exists", felde.exists(), "files", list(felde.rglob("*.html")))
for p in felde.rglob("*.html"):
    t = p.read_text(encoding="utf-8", errors="replace")
    print("FILE", p)
    print(" Service-PIN", "Service-PIN" in t or "EE36AKY" in t)
    print(" Wolfgang", t.count("Wolfgang"), "Kersten", t.count("Kersten"), "Axel", t.count("Axel Winkler"))
    print(" bannerright", t.count("bannerright"))
    print(" oberholz-team", t.count("oberholz-team"))
    for m in re.finditer(r"<img[^>]+>", t):
        tag = m.group(0)
        if any(k in tag for k in ("bannerright", "facepile", "avatar", "team", "t7a")):
            src = re.search(r'src="([^"]*)"', tag)
            alt = re.search(r'alt="([^"]*)"', tag)
            print(" ", src.group(1) if src else None, "|", alt.group(1) if alt else None)

# sample Service-PIN markup from a region page
for city in ["felde", "muenster", "essen", "bochum", "bielefeld"]:
    d = Path("public/regionen") / city
    if not d.exists():
        continue
    for p in d.rglob("*.html"):
        t = p.read_text(encoding="utf-8", errors="replace")
        if "Service-PIN" in t or "EE36AKY" in t:
            i = t.find("Service-PIN")
            if i < 0:
                i = t.find("EE36AKY")
            print("PIN SAMPLE", city, repr(t[max(0, i - 120) : i + 160]))
            break
    break
