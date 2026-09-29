"""Replace foreign banner portraits site-wide with Oberholz team images + names."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TEAM_DIR = ROOT / "public" / "media" / "oberholz-team"
MEDIA = ROOT / "public" / "media"

# Target widths for responsive banner folders
BANNER_SIZES = {
    "bannerright-780": 420,
    "bannerright-1024": 560,
    "bannerright-1440": 720,
    "bannerright-2400": 960,
}

# Oberholz people (cycle onto old banner slots)
TEAM = (
    ("michael-oberholz.png", "Michael Oberholz", "Inhaber & Sachverständiger"),
    ("felix-lesch.png", "Felix Lesch", "Immobilienberater"),
    ("michael-penn.png", "Michael Penn", "Immobilienberater"),
    ("pascal-kopp.png", "Pascal Kopp", "Transaktionsberater"),
    ("lubka-roeger.png", "Lubka Röger", "Immobilienberaterin"),
)

# Old EE-Experten portrait filenames in bannerright folders (people cutouts only)
OLD_PORTRAIT_FILES = (
    "t7a0115_kopie.png",
    "t7a3306.png",
    "t7a3373.png",
    "t7a3420.png",
    "t7a7869.png",
    "t7a7897.png",
    "t7a7913_1.png",
    "t7a9283_kopie.png",
    "t7a9489_copy.png",
)

# Old EE-Experten names → Oberholz team
PAIRED = (
    (re.compile(r"Kersten Streit", re.I), "Michael Oberholz"),
    (re.compile(r"Wolfgang Mayer", re.I), "Felix Lesch"),
    (re.compile(r"Axel Winkler", re.I), "Michael Penn"),
    (re.compile(r"Ren(?:é|&eacute;|&#233;) Mohr", re.I), "Pascal Kopp"),
    (re.compile(r"Christian Munz", re.I), "Lubka Röger"),
    (re.compile(r"Gebietsleiter(?:in)? Immobilienverkauf", re.I), "Immobilienberater"),
    (re.compile(r"Leitung Immobilienverkauf", re.I), "Inhaber &amp; Sachverständiger"),
    (re.compile(r"Leitung Immobilienvermittlung", re.I), "Inhaber &amp; Sachverständiger"),
    (re.compile(r"Leiter Immobilienverkauf", re.I), "Inhaber &amp; Sachverständiger"),
    (re.compile(r"streit_facepile\.jpg"), "oberholz_facepile.jpg"),
)

SKIP_DIRS = {"node_modules", ".git", "dist", "assets"}


def fit_portrait(src: Path, width: int) -> Image.Image:
    im = Image.open(src).convert("RGBA")
    # Scale to target width, keep aspect
    ratio = width / im.width
    height = max(1, round(im.height * ratio))
    return im.resize((width, height), Image.Resampling.LANCZOS)


def overwrite_banner_files() -> None:
    for folder, width in BANNER_SIZES.items():
        dest_dir = MEDIA / folder
        if not dest_dir.exists():
            continue
        for idx, filename in enumerate(OLD_PORTRAIT_FILES):
            team_file, name, role = TEAM[idx % len(TEAM)]
            src = TEAM_DIR / team_file
            if not src.exists():
                raise SystemExit(f"missing team image {src}")
            dest = dest_dir / filename
            if not dest.exists():
                print("skip missing", dest)
                continue
            out = fit_portrait(src, width)
            # Keep PNG with alpha
            out.save(dest, "PNG", optimize=True)
            print("wrote", dest.relative_to(ROOT), "from", team_file, out.size)


def patch_html_text() -> tuple[int, int]:
    files_changed = 0
    total_subs = 0
    html_files = [
        p
        for p in ROOT.rglob("*.html")
        if not any(part in SKIP_DIRS for part in p.parts)
    ]
    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text
        for pattern, repl in PAIRED:
            text, n = pattern.subn(repl, text)
            total_subs += n
        # Fix Lubka gender after generic role replace from Christian Munz slots
        text2 = text.replace(
            "Lubka Röger - Immobilienberater",
            "Lubka Röger - Immobilienberaterin",
        )
        text2 = text2.replace(
            "Lubka Röger – Immobilienberater",
            "Lubka Röger – Immobilienberaterin",
        )
        if text2 != text:
            total_subs += 1
            text = text2
        if text != original:
            path.write_text(text, encoding="utf-8")
            files_changed += 1
    return files_changed, total_subs


def main() -> None:
    overwrite_banner_files()
    # Also ensure facepile avatar is Oberholz wherever streit remains as file
    streit = MEDIA / "videocard_avatar" / "streit_facepile.jpg"
    ober = MEDIA / "videocard_avatar" / "oberholz_facepile.jpg"
    if streit.exists() and ober.exists():
        shutil.copyfile(ober, streit)
        print("overwrote streit_facepile.jpg with oberholz facepile")
    changed, subs = patch_html_text()
    print("html files changed", changed, "substitutions", subs)


if __name__ == "__main__":
    main()
