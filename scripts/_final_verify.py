from pathlib import Path
import re
h = Path("index.html").read_text(encoding="utf-8")
print("secondary tpl", h.count("immo-img-secondary-tpl"))
links = re.findall(r'<a class="stretched-link[^"]*" href="([^"]+)"', h)
immo = [l for l in links if l.startswith("/immobilien/")]
portal = [l for l in links if "immobilienscout24" in l]
print("card internal links", len(immo))
print("card portal links", len(portal))
print(immo[:3])
