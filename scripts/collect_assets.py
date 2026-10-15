"""Erzeugt Bild-PLATZHALTER in Original-Maßen (keine Originalbilder werden übernommen).
Pro Slot werden nur zwei Durchschnittsfarben (oben/unten) aus den lokalen Referenz-Screenshots gesampelt,
damit Helligkeit/Farbstimmung im Screenshot-Diff vergleichbar bleibt. Eigene Fotos einfach unter gleichem
Dateinamen (als .jpg) ablegen und in src/data/content.ts den Pfad anpassen."""
import json
from pathlib import Path
from PIL import Image
from _common import ROOT, REF, ANA

PUB = ROOT / "public" / "assets"
full = Image.open(REF / "full_1440.png").convert("RGB")
dom = json.loads((ANA / "dom_1440.json").read_text())

def avg(im, box):
    c = im.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0))
    return "#%02x%02x%02x" % c

def colors(im, x, y, w, h):
    return avg(im, (x, y, x + w, y + h // 2)), avg(im, (x, y + h // 2, x + w, y + h))

def svg(w, h, c1, c2, label):
    fs = max(10, round(min(w, h) * 0.045))
    text = "" if min(w, h) < 200 else (
        f'<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial, sans-serif" '
        f'font-size="{fs}" letter-spacing="{fs*0.15:.1f}" fill="#fff" fill-opacity=".55">{label}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
            f'<linearGradient id="l" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".08"/></linearGradient></defs>'
            f'<rect width="100%" height="100%" fill="url(#g)"/><rect width="100%" height="100%" fill="url(#l)"/>{text}</svg>')

def write(folder, name, w, h, c, label):
    p = PUB / folder; p.mkdir(parents=True, exist_ok=True)
    (p / f"{name}.svg").write_text(svg(w, h, c[0], c[1], label))

def imgs_in(node, out):
    if node.get("tag") == "img": out.append(node)
    for ch in node.get("c", []): imgs_in(ch, out)
    return out

all_imgs = []
for s in dom["sections"]: imgs_in(s, all_imgs)
by_alt = lambda frag: next(i for i in all_imgs if frag in (i.get("alt") or ""))
rect = lambda i: (i["r"]["x"], i["r"]["y"], i["r"]["w"], i["r"]["h"])

# Hero-Slides: Slide 1 aus Full-Page, weitere aus Mega-Menü-Screenshots (unterer, sichtbarer Hero-Bereich)
write("hero", "slide-1", 2720, 1166, colors(full, 40, 349, 1360, 583), "OBJEKTFOTO 1 · 21:9")
for n, i in enumerate((0, 1, 2, 3), start=2):
    im = Image.open(REF / f"megamenu_{i}_1440.png").convert("RGB")
    write("hero", f"slide-{n}", 2720, 1166, (avg(im, (40, 620, 1400, 760)), avg(im, (40, 760, 1400, 900))), f"OBJEKTFOTO {n} · 21:9")

# Hero-Teaser sind auf Desktop bei Scroll 0 unsichtbar → Farben aus dem Mobile-Original (dort sichtbar)
mob_path = ROOT / "screenshots" / "original" / "mobile-390_full.png"
mob = Image.open(mob_path).convert("RGB") if mob_path.exists() else full
for name, y in (("teaser-kaufen", 676), ("teaser-verkaufen", 784), ("teaser-karriere", 892)):
    write("properties", name, 120, 120, colors(mob, 28, y, 60, 60), "")

write("properties", "verkaufen", 1128, 752, colors(full, 156, 1849, 564, 376), "BILD · 3:2")
write("misc", "finanzierung-banner", 2880, 868, colors(full, 0, 2297, 1440, 434), "")
for name, frag in (("berlin", "Modernes, mehrstöckiges"), ("muenchen", "Historische europäische"), ("hamburg", "Malersiche Aussicht"),
                   ("frankfurt", "Altbaufassaden"), ("stuttgart", "Fluss, umgeben"), ("koeln", "Kölner Skyline")):
    write("cities", name, 1040, 696, colors(full, *rect(by_alt(frag))), name.upper())
write("careers", "karriere", 1128, 752, colors(full, 156, 4386, 564, 376), "BILD · 3:2")
for name, frag, big in (("galerie-1", "weiße Luxusvilla", True), ("galerie-2", "weißen Hemd mit Knopfleiste", False), ("galerie-3", "Polo-Spieler", False),
                        ("galerie-4", "Schnellboots", False), ("galerie-5", "metallischen Blazer", False), ("galerie-6", "Flugzeugs", True)):
    w, h = (1584, 891) if big else (644, 429)
    write("lifestyle", name, w, h, colors(full, *rect(by_alt(frag))), "BILD · 16:9" if big else "BILD · 3:2")
write("magazines", "magazin", 1128, 752, colors(full, 156, 6811, 564, 376), "MAGAZIN · 3:2")
for name, frag in (("avatar-1", "grauen Anzug"), ("avatar-2", "beigefarbenen")):
    write("misc", name, 144, 144, colors(full, *rect(by_alt(frag))), "")
for i in range(5):
    im = Image.open(REF / f"megamenu_{i}_1440.png").convert("RGB")
    box = (744, 176, 316, 236) if i < 4 else (1060, 150, 340, 240)
    if i == 4: im = im  # Unternehmen: Bild in Spalte 4
    write("misc", f"menu-promo-{i+1}", 632, 472, colors(im, *box), "")
print("placeholders ->", PUB)


# ---------- Unterseiten: Platzhalter je sichtbarem Bild (Maße ×2, Farben aus dem Referenz-Screenshot) ----------
def page_placeholders(slug):
    shot = REF / "pages" / f"{slug}_1440.png"
    data = ANA / "pages" / f"{slug}_1440.json"
    if not (shot.exists() and data.exists()): return []
    im = Image.open(shot).convert("RGB")
    d = json.loads(data.read_text())
    imgs = []
    for s in d["sections"]: imgs_in(s, imgs)
    seen, manifest = set(), []
    for i in imgs:
        x, y, w, h = rect(i)
        if w < 40 or h < 40 or x < 0 or x + w > 1440 or y + h > im.height: continue
        key = (x, y, w, h)
        if key in seen: continue
        seen.add(key)
        n = len(manifest) + 1
        name = f"img-{n:02d}"
        write(f"pages/{slug}", name, w * 2, h * 2, colors(im, x, y, w, h), f"BILD · {w}×{h}" if w >= 200 else "")
        manifest.append({"n": n, "file": f"/assets/pages/{slug}/{name}.svg", "rect": [x, y, w, h], "alt": (i.get("alt") or "")[:80]})
    (PUB / "pages" / slug).mkdir(parents=True, exist_ok=True)
    (ANA / "pages" / f"{slug}_images.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    return manifest

for slug in ("suche", "expose", "verkaufen", "bewertung", "makler-werden", "commercial", "ueber-uns", "standorte", "stadt", "magazin"):
    m = page_placeholders(slug)
    print(slug, len(m), "Platzhalter")


# ---------- Hero-Bilder der Unterseiten (CSS-Hintergründe / Videos, nicht im <img>-Manifest) ----------
HEROES = {
    "verkaufen": (720, 175, 680, 510), "makler-werden": (720, 175, 680, 510), "standorte": (720, 175, 680, 510),
    "commercial": (720, 347, 680, 510), "stadt": (720, 347, 680, 510), "ueber-uns": (40, 175, 1360, 408),
    "bewertung": (0, 135, 1440, 600), "magazin": (0, 0, 1440, 810),
}
EXTRA = {("magazin", "story"): (0, 2570, 1440, 810)}
for slug, (x, y, w, h) in HEROES.items():
    shot = REF / "pages" / f"{slug}_1440.png"
    if shot.exists():
        im = Image.open(shot).convert("RGB")
        label = "" if slug in ("magazin", "bewertung") else f"BILD · {w}×{h}"  # Hintergrundbilder mit Text darüber: ohne Beschriftung
        write(f"pages/{slug}", "hero", w * 2, h * 2, colors(im, x, y, w, h), label)
for (slug, name), (x, y, w, h) in EXTRA.items():
    im = Image.open(REF / "pages" / f"{slug}_1440.png").convert("RGB")
    write(f"pages/{slug}", name, w * 2, h * 2, colors(im, x, y, w, h), "")
print("Hero-Platzhalter ok")
