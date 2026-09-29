"""Cut only pure black studio backdrop. Keep the already-cleaned portraits intact."""

from __future__ import annotations

import os
from collections import deque

from PIL import Image

SRC_DIR = os.path.join(
    r"C:\Users\lsper\OneDrive - Dominik Scherwinsky\Desktop\httpsoberholz-immobilien website",
    "assets",
    "oberholz",
    "rotor-src",
)
OUT_DIR = os.path.join(
    r"C:\Users\lsper\OneDrive - Dominik Scherwinsky\Desktop\httpsoberholz-immobilien website",
    "public",
    "media",
    "oberholz-team",
)

# Attachment order: Oberholz, Penn, Kopp, Röger, Lesch → map to rotor slots.
SOURCES = (
    ("01.jpg", "michael-oberholz"),
    ("05.jpg", "felix-lesch"),
    ("02.jpg", "michael-penn"),
    ("03.jpg", "pascal-kopp"),
    ("04.jpg", "lubka-roeger"),
)


def knock_out(im: Image.Image) -> Image.Image:
    rgba = im.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def push(x: int, y: int) -> None:
        idx = y * width + x
        if seen[idx]:
            return
        r, g, b, _a = pixels[x, y]
        if max(r, g, b) > 3:
            return
        seen[idx] = 1
        queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        pixels[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                push(nx, ny)
    return rgba


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for filename, slug in SOURCES:
        image = Image.open(os.path.join(SRC_DIR, filename))
        cut = knock_out(image)
        if cut.width != 768:
            target_h = round(cut.height * 768 / cut.width)
            cut = cut.resize((768, target_h), Image.Resampling.LANCZOS)
        out = os.path.join(OUT_DIR, f"{slug}.png")
        cut.save(out, "PNG", optimize=True)
        print(slug, cut.size, os.path.getsize(out))


if __name__ == "__main__":
    main()
