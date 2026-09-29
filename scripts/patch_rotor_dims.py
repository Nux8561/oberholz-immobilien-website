from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")
dims = {
    "michael-oberholz": (900, 1200, "eager"),
    "felix-lesch": (900, 1188, "lazy"),
    "michael-penn": (900, 1200, "lazy"),
    "pascal-kopp": (900, 1200, "lazy"),
    "lubka-roeger": (900, 1200, "lazy"),
}
for slug, (w, h, loading) in dims.items():
    text = re.sub(
        rf'height="\d+" loading="{loading}" src="/media/oberholz-team/{slug}\.png" width="\d+"',
        f'height="{h}" loading="{loading}" src="/media/oberholz-team/{slug}.png" width="{w}"',
        text,
        count=1,
    )
path.write_text(text, encoding="utf-8")
print("ok")
