"""Baut die Oberholz-Hausschriften (brand/fonts/*.woff2) aus freien OFL-Grundschriften.

  Oberholz Antiqua  – Überschriften, Basis: Spectral SemiBold (OFL 1.1)
  Oberholz Grotesk  – Fließtext, Basis: Inter Tight (OFL 1.1), statische Schnitte 400/500/600/700

Eigene Anpassungen (Hausschnitt):
  • „Raute“ statt Rundpunkt: i/j-Punkte, Umlaute, Satzzeichen-Punkte und Aufzählungszeichen
    werden durch flächengleiche Rauten (auf der Spitze stehende Quadrate) ersetzt.
  • Eigene Namen, Metadaten und Herstellerkennung, Hinting entfernt (glatte Darstellung in allen Größen).
Die Grundschriften liegen in brand/fonts/source/ (beim ersten Lauf aus node_modules übernommen),
damit der Build ohne Fremdpakete reproduzierbar bleibt.

Aufruf:  python3 scripts/build_brand_fonts.py
"""
from __future__ import annotations

import math
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import ttProgram
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "fonts"
SRC = OUT / "source"
NM = ROOT / "node_modules"

VERSION = "1.000"
YEAR = 2026
VENDOR = "OBHZ"
OWNER = "Oberholz Immobilien, Münster"

SUBSETS = {
    # gleiche unicode-ranges wie die Grundschriften-Dateien (nur Latein + Latein erweitert)
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
             "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latin-ext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,"
                 "U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
}

FAMILIES = [
    {
        "family": "Oberholz Antiqua",
        "slug": "oberholz-antiqua",
        "base": "Spectral",
        "base_copyright": "Copyright 2017 The Spectral Project Authors (https://github.com/productiontype/Spectral)",
        "license_src": NM / "@fontsource/spectral/LICENSE",
        "license_dst": SRC / "OFL-Spectral.txt",
        "files": {s: (NM / f"@fontsource/spectral/files/spectral-{s}-600-normal.woff2", f"spectral-{s}-600.woff2") for s in SUBSETS},
        "weights": [600],
        "variable": False,
    },
    {
        "family": "Oberholz Grotesk",
        "slug": "oberholz-grotesk",
        "base": "Inter Tight",
        "base_copyright": "Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight)",
        "license_src": NM / "@fontsource-variable/inter-tight/LICENSE",
        "license_dst": SRC / "OFL-InterTight.txt",
        "files": {s: (NM / f"@fontsource-variable/inter-tight/files/inter-tight-{s}-wght-normal.woff2", f"inter-tight-{s}-wght.woff2") for s in SUBSETS},
        "weights": [400, 500, 600, 700],
        "variable": True,
    },
]

WEIGHT_NAMES = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}

# Zeichen, deren Rundpunkte zur Raute werden (einfache Glyphen; zusammengesetzte erben über Komponenten)
DOT_GLYPHS = {
    "i", "j", "fi", "f_i", "f_f_i", "f_j", "f_f_j", "period", "exclam", "exclamdown", "question", "questiondown",
    "periodcentered", "bullet", "dieresis", "dotaccent", "dieresiscomb", "dieresiscomb.case", "dotaccentcomb",
    "dotaccentcomb.case", "dotbelowcomb", "uni0307", "uni0308", "uni0323", "ldot", "Ldot", "exclamdbl",
}
DIAMOND_SCALE = 1.25  # halbe Diagonale = 0,625 × Punktdurchmesser → flächengleich zum Kreis


def ensure_sources() -> None:
    """Grundschriften + Lizenzen einmalig nach brand/fonts/source kopieren."""
    SRC.mkdir(parents=True, exist_ok=True)
    for fam in FAMILIES:
        if not fam["license_dst"].exists():
            shutil.copyfile(fam["license_src"], fam["license_dst"])
        for src, name in fam["files"].values():
            dst = SRC / name
            if not dst.exists():
                shutil.copyfile(src, dst)


def signed_area(pts: list[tuple[float, float]]) -> float:
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) / 2


def is_round_dot(pts: list[tuple[float, float]], upm: int, big: bool) -> bool:
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    if not h or not (0.82 <= w / h <= 1.22) or len(pts) < 8:
        return False
    size = (w + h) / 2 / upm
    if not (0.04 <= size <= (0.36 if big else 0.2)):
        return False
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    radii = [math.hypot(x - cx, y - cy) for x, y in pts]
    return max(radii) / min(radii) < 1.6


def diamondize(font: TTFont) -> list[str]:
    """Ersetzt Rundpunkte durch Rauten. Gibt die geänderten Glyphen zurück."""
    glyf, hmtx, upm = font["glyf"], font["hmtx"], font["head"].unitsPerEm
    changed = []
    for name in sorted(DOT_GLYPHS & set(font.getGlyphOrder())):
        g = glyf[name]
        if g.isComposite() or g.numberOfContours <= 0:
            continue
        coords, ends, flags = g.getCoordinates(glyf)
        new_coords, new_ends, new_flags, start, hit = [], [], [], 0, False
        for end in ends:
            pts = [tuple(c) for c in coords[start:end + 1]]
            if is_round_dot(pts, upm, big=name == "bullet"):
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
                r = (max(xs) - min(xs) + max(ys) - min(ys)) / 4 * DIAMOND_SCALE
                diamond = [(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)]  # im Uhrzeigersinn
                if (signed_area(diamond) > 0) != (signed_area(pts) > 0):
                    diamond.reverse()
                pts, fl, hit = [(round(x), round(y)) for x, y in diamond], [1] * 4, True
            else:
                fl = list(flags[start:end + 1])
            new_coords += pts
            new_flags += fl
            new_ends.append(len(new_coords) - 1)
            start = end + 1
        if not hit:
            continue
        from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
        g.coordinates = GlyphCoordinates(new_coords)
        g.endPtsOfContours = new_ends
        g.flags = bytearray(new_flags)
        g.program = ttProgram.Program()
        g.program.fromBytecode(b"")
        g.recalcBounds(glyf)
        adv, _ = hmtx[name]
        hmtx[name] = (adv, g.xMin)
        changed.append(name)
    return changed


def dehint(font: TTFont) -> None:
    for tag in ("fpgm", "prep", "cvt ", "hdmx", "LTSH", "VDMX"):
        if tag in font:
            del font[tag]
    glyf = font["glyf"]
    for name in font.getGlyphOrder():
        g = glyf[name]
        if hasattr(g, "program"):
            g.program = ttProgram.Program()
            g.program.fromBytecode(b"")
    gasp = newTable("gasp")
    gasp.version = 1
    gasp.gaspRange = {0xFFFF: 0x000F}
    font["gasp"] = gasp
    font["head"].flags &= ~(1 << 3 | 1 << 4)


def rename(font: TTFont, fam: dict, weight: int) -> None:
    style = WEIGHT_NAMES[weight]
    family, ps_family = fam["family"], fam["family"].replace(" ", "")
    ribbi = weight in (400, 700)
    legacy_family = family if ribbi else f"{family} {style}"
    legacy_style = style if ribbi else "Regular"
    name = font["name"]
    name.names = []
    entries = {
        0: f"{fam['base_copyright']}. Hausschnitt © {YEAR} {OWNER}.",
        1: legacy_family,
        2: legacy_style,
        3: f"{VERSION};{VENDOR};{ps_family}-{style}",
        4: f"{family} {style}",
        5: f"Version {VERSION}; Oberholz-Hausschnitt auf Basis von {fam['base']}",
        6: f"{ps_family}-{style}",
        8: OWNER,
        10: f"Hausschrift von {OWNER}. Abgeleitet von {fam['base']} (SIL Open Font License 1.1); "
            "Rautenpunkte und Metadaten angepasst.",
        13: "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
            "This license is available with a FAQ at: https://openfontlicense.org",
        14: "https://openfontlicense.org",
    }
    if not ribbi:
        entries[16] = family
        entries[17] = style
    for nid, text in entries.items():
        name.setName(text, nid, 3, 1, 0x409)
    os2 = font["OS/2"]
    os2.achVendID = VENDOR
    os2.usWeightClass = weight
    # fsSelection: Bit 5 Bold, Bit 6 Regular, Bit 7 USE_TYPO_METRICS beibehalten
    sel = os2.fsSelection & ~(1 << 0 | 1 << 5 | 1 << 6)
    sel |= (1 << 5) if weight == 700 else (1 << 6) if weight == 400 else 0
    os2.fsSelection = sel
    font["head"].macStyle = 1 if weight == 700 else 0
    font["head"].fontRevision = float(VERSION)
    if "STAT" in font:
        del font["STAT"]
    font["post"].formatType = 2.0


def build() -> list[dict]:
    ensure_sources()
    shutil.copyfile(FAMILIES[0]["license_dst"], OUT / "OFL.txt")
    faces = []
    for fam in FAMILIES:
        for subset, (_, src_name) in fam["files"].items():
            for weight in fam["weights"]:
                font = TTFont(SRC / src_name)
                if fam["variable"]:
                    font = instancer.instantiateVariableFont(font, {"wght": weight}, updateFontNames=False)
                changed = diamondize(font)
                dehint(font)
                rename(font, fam, weight)
                font.flavor = "woff2"
                out = OUT / f"{fam['slug']}-{weight}-{subset}.woff2"
                font.save(out)
                faces.append({"family": fam["family"], "weight": weight, "subset": subset, "file": out.name})
                print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:5.1f} KB  Rauten: {', '.join(changed)}")
    return faces


def write_css(faces: list[dict]) -> None:
    css = ["/* Oberholz-Hausschriften – erzeugt von scripts/build_brand_fonts.py, nicht von Hand ändern. */"]
    for f in faces:
        css.append(
            "@font-face {\n"
            f"  font-family: '{f['family']}';\n"
            "  font-style: normal;\n"
            "  font-display: swap;\n"
            f"  font-weight: {f['weight']};\n"
            f"  src: url('../../brand/fonts/{f['file']}') format('woff2');\n"
            f"  unicode-range: {SUBSETS[f['subset']]};\n"
            "}"
        )
    (ROOT / "src" / "styles" / "fonts.css").write_text("\n".join(css) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_css(build())
