"""Pixel-Diff Original vs. lokal (Pillow): diff.png (rot = Abweichung), overlay.png (50/50), Kennzahlen.
Aufruf: python3 scripts/visual_diff.py [muster]   – vergleicht alle gleichnamigen PNGs in screenshots/original|local.
Zusätzlich section-weise Diffs für Full-Page-Screenshots anhand der Referenz-Section-Grenzen."""
import json, sys
from pathlib import Path
from PIL import Image, ImageChops
from _common import SHOTS, ANA

THRESH = 32  # Kanal-Differenz ab der ein Pixel als „abweichend“ zählt (Antialiasing ignorieren)

def compare(a_path, b_path, out_name, box=None):
    a = Image.open(a_path).convert("RGB"); b = Image.open(b_path).convert("RGB")
    W, H = max(a.width, b.width), max(a.height, b.height)
    if box: a, b = a.crop(box), b.crop(box); W, H = box[2] - box[0], box[3] - box[1]
    pa = Image.new("RGB", (W, H), "white"); pa.paste(a, (0, 0))
    pb = Image.new("RGB", (W, H), "white"); pb.paste(b, (0, 0))
    diff = ImageChops.difference(pa, pb)
    gray = diff.convert("L")
    mask = gray.point(lambda v: 255 if v > THRESH else 0)
    hist = gray.histogram()
    mae = sum(i * c for i, c in enumerate(hist)) / (W * H) / 255 * 100
    changed = mask.histogram()[255] / (W * H) * 100
    bbox = mask.getbbox()
    vis = Image.blend(pa.convert("L").convert("RGB"), Image.new("RGB", (W, H), "white"), 0.6)
    vis.paste(Image.new("RGB", (W, H), (230, 0, 0)), (0, 0), mask)
    vis.save(SHOTS / "diff" / f"{out_name}.png")
    Image.blend(pa, pb, 0.5).save(SHOTS / "overlay" / f"{out_name}.png")
    return {"pixel_diff_pct": round(changed, 2), "mae_pct": round(mae, 2), "bbox": bbox, "size": [W, H]}

SECTION_NAMES = ["Hero (Suche+Slider+Teaser)", "Verkaufen Intro", "Vorteile", "Verkaufen CTA", "Finanzierungs-Banner", "Städte",
                 "Karriere Intro", "Karriere CTA", "Lifestyle Intro", "Lifestyle-Galerie", "Magazin Intro", "Magazin CTA",
                 "Newsletter", "Weitere Themen", "Kontakt"]

def image_rects(dom):
    """Alle Bild-/Video-Flächen der Referenz (werden für den Layout-Diff ausgeblendet)."""
    out = []
    def walk(n):
        if n.get("tag") in ("img", "video", "picture") or "aspect-ratio" in n.get("s", {}):
            r = n["r"]; out.append((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
        for c in n.get("c", []): walk(c)
    for sec in dom["sections"]: walk(sec)
    return out

def masked_compare(a_path, b_path, rects, out_name):
    from PIL import ImageDraw
    a = Image.open(a_path).convert("RGB"); b = Image.open(b_path).convert("RGB")
    for im in (a, b):
        d = ImageDraw.Draw(im)
        for r in rects: d.rectangle(r, fill=(128, 128, 128))
    tmp_a, tmp_b = SHOTS / "diff" / "_ma.png", SHOTS / "diff" / "_mb.png"
    a.save(tmp_a); b.save(tmp_b)
    res = compare(tmp_a, tmp_b, out_name)
    tmp_a.unlink(); tmp_b.unlink()
    return res

def main():
    pat = sys.argv[1] if len(sys.argv) > 1 else ""
    report = {}
    for a in sorted((SHOTS / "original").glob(f"*{pat}*.png" if pat else "*.png")):
        b = SHOTS / "local" / a.name
        if not b.exists(): continue
        report[a.stem] = compare(a, b, a.stem)
        print(f"{a.stem:28s} diff {report[a.stem]['pixel_diff_pct']:6.2f}%  MAE {report[a.stem]['mae_pct']:5.2f}%")
        # Section-Diffs für Full-Page
        if a.stem.endswith("_full"):
            w = Image.open(a).width
            dom_file = ANA / f"dom_{w}.json"
            if not dom_file.exists(): continue
            dom = json.loads(dom_file.read_text())
            m = masked_compare(a, b, image_rects(dom), f"{a.stem}__layout")
            report[f"{a.stem}__layout"] = m
            print(f"   {'LAYOUT/TEXT (ohne Bildflächen)':28s} diff {m['pixel_diff_pct']:6.2f}%  MAE {m['mae_pct']:5.2f}%")
            boxes = [("Header", dom["header"]["r"])] + list(zip(SECTION_NAMES, [s["r"] for s in dom["sections"]])) + [("Footer", dom["footer"]["r"])]
            for name, r in boxes:
                key = f"{a.stem}__{name.split(' ')[0].lower()}"
                res = compare(a, b, key, (0, r["y"], w, r["y"] + r["h"]))
                report[key] = res
                print(f"   {name:28s} diff {res['pixel_diff_pct']:6.2f}%  MAE {res['mae_pct']:5.2f}%")
    # Unterseiten-Templates (Full-Page 1440): Referenz vs. lokal
    if not pat or pat == "pages":
        from _common import REF
        for ref in sorted((REF / "pages").glob("*_1440.png")):
            slug = ref.stem.rsplit("_", 1)[0]
            loc = SHOTS / "local" / f"page_{slug}_1440.png"
            if not loc.exists(): continue
            r = compare(ref, loc, f"page_{slug}_1440")
            report[f"page_{slug}_1440"] = r
            print(f"page {slug:24s} diff {r['pixel_diff_pct']:6.2f}%  MAE {r['mae_pct']:5.2f}%")
    (SHOTS / "diff" / "report.json").write_text(json.dumps(report, indent=1))

if __name__ == "__main__":
    main()
