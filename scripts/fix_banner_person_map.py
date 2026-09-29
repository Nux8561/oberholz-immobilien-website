"""Re-overwrite banner portraits to match HTML alt names (not blind cycle)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "public" / "media"
TEAM_DIR = MEDIA / "oberholz-team"

BANNER_SIZES = {
    "bannerright-780": 420,
    "bannerright-1024": 560,
    "bannerright-1440": 720,
    "bannerright-2400": 960,
}

# Derived from img alt attributes across many pages
FILE_TO_TEAM = {
    "t7a0115_kopie.png": "pascal-kopp.png",       # Pascal Kopp (ex René Mohr)
    "t7a3373.png": "michael-oberholz.png",        # Michael Oberholz
    "t7a3420.png": "michael-oberholz.png",        # Michael Oberholz (main hero slot)
    "t7a7897.png": "felix-lesch.png",             # Felix Lesch (ex Wolfgang Mayer)
    "t7a7913_1.png": "michael-penn.png",          # Michael Penn (ex Axel Winkler)
    "t7a9283_kopie.png": "lubka-roeger.png",      # Lubka Röger (ex Christian Munz)
    # Rare / few alt hits — keep distinct team faces for remaining slots
    "t7a3306.png": "felix-lesch.png",
    "t7a7869.png": "lubka-roeger.png",
    "t7a9489_copy.png": "pascal-kopp.png",
}


def fit(src: Path, width: int) -> Image.Image:
    im = Image.open(src).convert("RGBA")
    ratio = width / im.width
    height = max(1, round(im.height * ratio))
    return im.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    n = 0
    for folder, width in BANNER_SIZES.items():
        dest_dir = MEDIA / folder
        if not dest_dir.exists():
            continue
        for filename, team_file in FILE_TO_TEAM.items():
            src = TEAM_DIR / team_file
            dest = dest_dir / filename
            if not dest.exists():
                print("skip missing", dest.relative_to(ROOT))
                continue
            out = fit(src, width)
            out.save(dest, "PNG", optimize=True)
            print("wrote", dest.relative_to(ROOT), "<-", team_file, out.size)
            n += 1
    print("done", n)


if __name__ == "__main__":
    main()
