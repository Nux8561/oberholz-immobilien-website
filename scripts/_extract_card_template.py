from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
rendered = (root / "analysis/rendered.html").read_text(encoding="utf-8", errors="replace")

# extract one full immo-card from rendered analysis
m = re.search(
    r'(<div class="col-12 col-md-6 col-lg-4"[^>]*>\s*<article class="card immo-card.*?</article>\s*</div>)',
    rendered,
    re.S,
)
out = root / "assets/oberholz/_sample_card.html"
if m:
    out.write_text(m.group(1), encoding="utf-8")
    print("card written", len(m.group(1)))
    # find secondary part
    sec = re.search(r"immo-img-secondary-tpl.*?</template>", m.group(1), re.S)
    print("has secondary tpl", bool(sec))
    if sec:
        print(sec.group(0)[:500])
    href = re.search(r'href="([^"]+)"', m.group(1))
    print("href", href.group(1) if href else None)
else:
    print("NO CARD FOUND")
    # try looser
    idx = rendered.find("immo-img-secondary-tpl")
    print("idx", idx)
    if idx > 0:
        print(rendered[idx - 400 : idx + 800])

# extract key regions from detail page
detail = (root / "public/immobilien/krefeld/charmantes-familienhaus-in-krefeld-linn-5835561.html").read_text(encoding="utf-8", errors="replace")
# find object gallery block
for label, pat in [
    ("hero", r'object-hero-780/[^"\s]+'),
    ("thumb", r'object-thumb-780/[^"\s]+'),
    ("price", r'Kaufpreis|Kaltmiete|Preis'),
    ("id", r'5835561'),
]:
    print(label, len(re.findall(pat, detail)))

# dump a slice around first object-hero for structure
i = detail.find("object-hero-780")
Path(root / "assets/oberholz/_sample_detail_slice.html").write_text(detail[max(0, i - 500) : i + 4000], encoding="utf-8")
print("slice written")

# list media folders for objects
media = root / "public/media"
for name in ["object-hero-780", "object-thumb-780", "object-card", "listings"]:
    p = media / name
    if p.exists():
        files = list(p.glob("*"))
        print(name, "count", len(files), "sample", [f.name for f in files[:5]])
