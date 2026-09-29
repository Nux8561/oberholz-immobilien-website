"""Pixel-diff original vs local screenshots."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "reference"
LOCAL = ROOT / "screenshots" / "local"
DIFF = ROOT / "screenshots" / "diff"


def diff_pair(original: Path, local: Path, out_dir: Path) -> dict:
    img_a = Image.open(original).convert("RGB")
    img_b = Image.open(local).convert("RGB")
    width = min(img_a.width, img_b.width)
    height = max(img_a.height, img_b.height)
    canvas_a = Image.new("RGB", (width, height), (255, 255, 255))
    canvas_b = Image.new("RGB", (width, height), (255, 0, 0))
    canvas_a.paste(img_a.crop((0, 0, width, min(height, img_a.height))), (0, 0))
    canvas_b.paste(img_b.crop((0, 0, width, min(height, img_b.height))), (0, 0))
    if img_b.height < height:
        draw = ImageDraw.Draw(canvas_b)
        draw.rectangle((0, img_b.height, width, height), fill=(255, 0, 0))
    if img_a.height < height:
        draw = ImageDraw.Draw(canvas_a)
        draw.rectangle((0, img_a.height, width, height), fill=(0, 0, 255))

    diff = ImageChops.difference(canvas_a, canvas_b)
    extrema = diff.getextrema()
    stat = diff.convert("L")
    hist = stat.histogram()
    different = sum(hist[8:])
    total = width * height
    mean = sum(i * count for i, count in enumerate(hist)) / total
    overlay = Image.blend(canvas_a, canvas_b, 0.5)
    heat = ImageEnhance.Brightness(diff).enhance(4)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = original.stem
    diff.save(out_dir / f"{name}-diff.png")
    overlay.save(out_dir / f"{name}-overlay.png")
    heat.save(out_dir / f"{name}-heat.png")
    return {
        "file": original.name,
        "original_size": [img_a.width, img_a.height],
        "local_size": [img_b.width, img_b.height],
        "percentage_difference": round(different / total * 100, 3),
        "mean_pixel_error": round(mean, 3),
        "different_pixels": different,
        "total_pixels": total,
    }


def main() -> None:
    results = []
    for original in sorted(ORIGINAL.rglob("*-full.png")):
        local = LOCAL / original.relative_to(ORIGINAL)
        if not local.exists():
            print("missing local", local)
            continue
        out = DIFF / original.parent.name
        stats = diff_pair(original, local, out)
        results.append({"viewport": original.parent.name, **stats})
        print(original.parent.name, stats["percentage_difference"], "mean", stats["mean_pixel_error"])
    (DIFF / "report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
