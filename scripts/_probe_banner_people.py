from pathlib import Path
import re

root = Path(".")
# Sample a few HTML files for person name + image pairs
samples = [
    root / "index.html",
    *list((root / "public" / "regionen").rglob("*.html"))[:3],
]
# Also search quickly with ripgrep via python on index only for alt texts
text = (root / "index.html").read_text(encoding="utf-8", errors="replace")
pairs = re.findall(
    r'(?:alt|title)="([^"]{5,80})"[^>]*src="(/media/bannerright-\d+/[^"]+)"|src="(/media/bannerright-\d+/[^"]+)"[^>]*(?:alt|title)="([^"]{5,80})"',
    text,
)
print("index pairs", len(pairs))
for p in pairs[:20]:
    print(p)

# collect unique filename -> alt from index
for m in re.finditer(r'<img[^>]+>', text):
    tag = m.group(0)
    if "bannerright" not in tag and "oberholz-team" not in tag:
        continue
    src = re.search(r'src="([^"]+)"', tag)
    alt = re.search(r'alt="([^"]*)"', tag)
    title = re.search(r'title="([^"]*)"', tag)
    print("IMG", src.group(1) if src else None, "|", alt.group(1) if alt else None, "|", title.group(1) if title else None)
