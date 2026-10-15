"""Erzeugt aus den freigestellten Teamfotos (public/assets/oberholz/media/oberholz-team/*.png)
1) das Gruppenbild team/team-gruppe.jpg und 2) quadratische Gesichtsausschnitte team/face-<name>.jpg für Avatare."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public/assets/oberholz/media/oberholz-team"
OUT = ROOT / "public/assets/oberholz/media/team"
OUT.mkdir(parents=True, exist_ok=True)
TOP, BOT = (246, 242, 234), (234, 227, 212)


def cream(w, h):
    bg = Image.new("RGB", (w, h))
    for y in range(h):
        t = y / max(1, h - 1)
        bg.paste(tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)), (0, y, w, y + 1))
    return bg.convert("RGBA")


def group():
    order = [("lubka-roeger", .15), ("michael-penn", .85), ("felix-lesch", .33), ("pascal-kopp", .67), ("michael-oberholz", .5)]
    W, H = 1500, 1000
    bg = cream(W, H)
    for name, cx in order:
        im = Image.open(SRC / f"{name}.png").convert("RGBA")
        h = 900 if name == "michael-oberholz" else 840
        im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
        bg.alpha_composite(im, (int(W * cx - im.width / 2), H - h + 60))
    bg.convert("RGB").save(OUT / "team-gruppe.jpg", quality=86)


def face(name):
    im = Image.open(SRC / f"{name}.png").convert("RGBA")
    a = im.getchannel("A")
    W, H = im.size
    rows = [y for y in range(H) if sum(1 for x in range(0, W, 4) if a.getpixel((x, y)) > 128) > 3]
    y0 = rows[0]
    # Kopfbreite aus den Zeilen knapp unter dem Scheitel
    xs = [x for y in range(int(y0 + .05 * H), int(y0 + .11 * H), 6) for x in range(0, W, 3) if a.getpixel((x, y)) > 128]
    xl, xr = min(xs), max(xs)
    cx, hw = (xl + xr) / 2, xr - xl
    side = hw * 2.1
    top = y0 - side * .12
    pad = 400  # Rand oberhalb des Kopfes mit Creme auffüllen
    box = (int(cx - side / 2), int(top) + pad, int(cx + side / 2), int(top + side) + pad)
    bg = cream(W, H + pad)
    bg.alpha_composite(im, (0, pad))
    bg.crop(box).convert("RGB").resize((320, 320), Image.LANCZOS).save(OUT / f"face-{name}.jpg", quality=88)


if __name__ == "__main__":
    group()
    for f in SRC.glob("*.png"):
        face(f.stem)
    print("ok", sorted(p.name for p in OUT.iterdir()))
