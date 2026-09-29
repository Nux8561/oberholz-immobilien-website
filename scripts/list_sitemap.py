import requests
from collections import Counter
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

r = requests.get("https://www.immobilien-experten.de/sitemap.xml", timeout=60)
r.raise_for_status()
root = ET.fromstring(r.content)
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [el.text.strip() for el in root.findall(".//s:loc", ns) if el.text]
print("urls", len(locs))
buckets = Counter()
for loc in locs:
    path = urlparse(loc).path
    parts = [p for p in path.split("/") if p]
    key = parts[0] if parts else "/"
    buckets[key] += 1
for key, count in buckets.most_common(40):
    print(f"{count:6} {key}")
open("analysis/sitemap_urls.txt", "w", encoding="utf-8").write("\n".join(locs))
