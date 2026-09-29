from PIL import Image
from pathlib import Path

pairs = [
    ("1440x900", 1200, 1700),
    ("390x844", 680, 1100),
    ("768x1024", 3920, 4300),
]
for name, y0, y1 in pairs:
    for kind, folder in (("original", Path("reference")), ("local", Path("screenshots/local"))):
        src = folder / name / f"{name}-full.png"
        img = Image.open(src)
        crop = img.crop((0, y0, img.width, min(img.height, y1)))
        out = Path("screenshots/diff") / f"crop-{name}-{kind}-{y0}.png"
        crop.save(out)
        print("saved", out, crop.size)
