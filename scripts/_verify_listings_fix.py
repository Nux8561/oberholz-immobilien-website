from pathlib import Path
import re

html = Path("index.html").read_text(encoding="utf-8")
i = html.find('id="angebote"')
chunk = html[i : i + 8000]
print("secondary-tpl", chunk.count("immo-img-secondary-tpl"))
print("portal expose", len(re.findall(r"portal\.immobilienscout24\.de/expose", chunk)))
print("internal", re.findall(r'href="(/immobilien/[^"]+)"', chunk)[:6])
print("thumb001", chunk.count("_001.jpg"))
# check first detail exists
href = re.search(r'href="(/immobilien/[^"]+)"', chunk).group(1)
path = Path("public") / href.lstrip("/")
print("detail exists", path.exists(), path)
detail = path.read_text(encoding="utf-8")
print("gallery imgs", detail.count("object-zoom-780"))
print("Objektbeschreibung", "Objektbeschreibung" in detail)
