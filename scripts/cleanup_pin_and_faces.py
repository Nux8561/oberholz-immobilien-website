"""Site-wide: remove Service-PIN, swap leftover faces/names (Ute Schorpp, facepile)."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "public" / "media"
TEAM_DIR = MEDIA / "oberholz-team"

SKIP_DIRS = {"node_modules", ".git", "dist", "assets", ".cursor"}

# Service-PIN footer (PIN code varies per page)
PIN_RE = re.compile(
    r'\s*<div class="text-center d-block">\s*'
    r'<span class="text-muted">Service-PIN:\s*'
    r'<strong class="text-md"[^>]*>[^<]*</strong>\s*'
    r"</span>\s*</div>",
    re.IGNORECASE,
)

NAME_REPLACEMENTS: list[tuple[str, str]] = [
    ("Kersten Streit", "Michael Oberholz"),
    ("Wolfgang Mayer", "Felix Lesch"),
    ("Axel Winkler", "Michael Penn"),
    ("René Mohr", "Pascal Kopp"),
    ("Rene Mohr", "Pascal Kopp"),
    ("Ren&eacute; Mohr", "Pascal Kopp"),
    ("Christian Munz", "Lubka Röger"),
    ("Ute Schorpp", "Lubka Röger"),
    ("Teamleiterin Kundenberatung", "Immobilienberaterin"),
    ("Gebietsleiterin Immobilienverkauf", "Immobilienberaterin"),
    ("Gebietsleiter Immobilienverkauf", "Immobilienberater"),
    ("Leitung Immobilienverkauf", "Inhaber &amp; Sachverständiger"),
    ("Leitung Immobilienvermittlung", "Inhaber &amp; Sachverständiger"),
    ("Leiter Immobilienverkauf", "Inhaber &amp; Sachverständiger"),
    ("streit_facepile.jpg", "oberholz_facepile.jpg"),
    ("streit_facepile_1.jpg", "oberholz_facepile.jpg"),
    ("team_schorpp.jpg", "lubka-roeger.jpg"),
    (r"\/media\/team\/team_schorpp.jpg", r"\/media\/team\/lubka-roeger.jpg"),
    ("/media/team/team_schorpp.jpg", "/media/team/lubka-roeger.jpg"),
]

# Facepile / avatar / team files to overwrite with Oberholz portraits
FACE_MAP: list[tuple[str, str]] = [
    # (relative under public/media, team source png)
    ("facepile/profilbild_winkler.jpg", "michael-penn.png"),
    ("facepile/profilbild_mayer.jpg", "felix-lesch.png"),
    ("facepile/streit_facepile.jpg", "michael-oberholz.png"),
    ("facepile/streit_facepile_1.jpg", "michael-oberholz.png"),
    ("facepile/team_mohr.jpg", "pascal-kopp.png"),
    ("facepile/munz_ie.png", "lubka-roeger.png"),
    ("facepile/oberholz_facepile.jpg", "michael-oberholz.png"),
    ("team/streit_facepile.jpg", "michael-oberholz.png"),
    ("team/oberholz_facepile.jpg", "michael-oberholz.png"),
    ("team/lubka-roeger.jpg", "lubka-roeger.png"),
    ("team/team_schorpp.jpg", "lubka-roeger.png"),
]


def save_as(src: Path, dest: Path, max_width: int = 480) -> None:
    im = Image.open(src).convert("RGBA")
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize(
            (max_width, max(1, round(im.height * ratio))),
            Image.Resampling.LANCZOS,
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    suffix = dest.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        # RGB on white for JPEG
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        bg.save(dest, "JPEG", quality=88, optimize=True)
    else:
        im.save(dest, "PNG", optimize=True)


def overwrite_faces() -> int:
    n = 0
    for rel, team_file in FACE_MAP:
        src = TEAM_DIR / team_file
        if not src.exists():
            raise SystemExit(f"missing team image: {src}")
        dest = MEDIA / rel
        save_as(src, dest)
        print("face", dest.relative_to(ROOT))
        n += 1

    # hashed videocard avatars
    vdir = MEDIA / "videocard_avatar"
    if vdir.exists():
        mapping = {
            "streit_facepile": "michael-oberholz.png",
            "profilbild_mayer": "felix-lesch.png",
            "profilbild_winkler": "michael-penn.png",
            "team_mohr": "pascal-kopp.png",
            "munz_ie": "lubka-roeger.png",
        }
        for path in vdir.iterdir():
            if not path.is_file():
                continue
            lower = path.name.lower()
            for key, team_file in mapping.items():
                if key in lower:
                    save_as(TEAM_DIR / team_file, path)
                    print("avatar", path.relative_to(ROOT))
                    n += 1
                    break
    return n


def patch_html(path: Path) -> tuple[int, int]:
    """Returns (pin_removed, name_hits)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0, 0
    original = text
    text, pin_n = PIN_RE.subn("", text)
    # Also catch PIN without wrapping quirks
    if "Service-PIN" in text:
        text2, n2 = re.subn(
            r'<span class="text-muted">\s*Service-PIN:\s*'
            r'<strong class="text-md"[^>]*>[^<]*</strong>\s*</span>',
            "",
            text,
            flags=re.I,
        )
        pin_n += n2
        text = text2

    name_hits = 0
    for old, new in NAME_REPLACEMENTS:
        if old in text:
            c = text.count(old)
            text = text.replace(old, new)
            name_hits += c

    text = text.replace(
        "Lubka Röger - Immobilienberater",
        "Lubka Röger - Immobilienberaterin",
    )
    text = text.replace(
        "Lubka Röger – Immobilienberater",
        "Lubka Röger – Immobilienberaterin",
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
    return pin_n, name_hits


def iter_html() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return out


def main() -> None:
    faces = overwrite_faces()
    print("faces_written", faces)

    files = iter_html()
    print("html_files", len(files))
    pin_total = 0
    name_total = 0
    changed = 0
    for i, path in enumerate(files, 1):
        pin_n, name_n = patch_html(path)
        if pin_n or name_n:
            changed += 1
            pin_total += pin_n
            name_total += name_n
        if i % 2000 == 0:
            print(f"progress {i}/{len(files)} changed {changed}")

    print("done changed", changed, "pins", pin_total, "names", name_total)

    # Verify Felde
    for p in (ROOT / "public/regionen/felde").rglob("*.html"):
        t = p.read_text(encoding="utf-8", errors="replace")
        print(
            "verify",
            p.name,
            "PIN",
            "Service-PIN" in t,
            "Ute",
            "Ute Schorpp" in t,
            "Schorpp",
            "Schorpp" in t,
            "winkler_path",
            "profilbild_winkler" in t,
        )


if __name__ == "__main__":
    main()
