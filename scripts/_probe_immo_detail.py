from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text(encoding="utf-8")
print("secondary count", html.count("immo-img-secondary"))
print("listing imgs", html.count("/media/oberholz-listings/"))
links = re.findall(r'href="(/immobilien/[^"]+)"', html)
print("on-site immobilien links in index", len(links), links[:3])
portal = re.findall(r'href="(https://portal\.immobilienscout24\.de/[^"]+)"', html)
print("portal links", len(portal), portal[:3])

# sample detail page structure
p = root / "public/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html"
t = p.read_text(encoding="utf-8", errors="replace")
print("detail bytes", len(t))
m = re.search(r"<title>(.*?)</title>", t, re.I | re.S)
print("title", (m.group(1)[:140] if m else None))

# find gallery / carousel markers
for pat in [
    r"carousel",
    r"gallery",
    r"objekt-galerie",
    r"swiper",
    r"owl-carousel",
    r"data-bs-ride",
    r"immo-detail",
    r"expose",
]:
    print(pat, t.lower().count(pat.lower()))

# extract interesting chunks around h1 and images
h1 = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.I | re.S)
print("h1", re.sub(r"<[^>]+>", "", h1.group(1))[:160] if h1 else None)
imgs = re.findall(r'src="([^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"', t, re.I)
print("img count", len(imgs))
for u in imgs[:12]:
    print(" ", u[:140])

# look for secondary template in analysis
for path in [
    root / "analysis" / "rendered.html",
    root / "analysis" / "assets.json",
]:
    if path.exists():
        txt = path.read_text(encoding="utf-8", errors="replace")
        print(path.name, "secondary", txt.count("immo-img-secondary"), "immo-card", txt.count("immo-card"))
