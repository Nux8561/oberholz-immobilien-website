"""Find vertical bands with the most pixel difference."""
from pathlib import Path
from PIL import Image

root = Path("screenshots/diff")
for heat in sorted(root.glob("*/*-heat.png")):
    img = Image.open(heat).convert("L")
    w, h = img.size
    pixels = img.load()
    band = 80
    scores = []
    for y0 in range(0, h, band):
        y1 = min(h, y0 + band)
        total = 0
        for y in range(y0, y1):
            for x in range(0, w, 4):
                total += pixels[x, y]
        scores.append((total, y0, y1))
    scores.sort(reverse=True)
    top = scores[:4]
    print(heat.parent.name, "top bands", [(s[1], s[2], s[0]) for s in top])
