from collections import Counter
import re
from pathlib import Path
from bs4 import BeautifulSoup

html = Path("analysis/rendered.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "lxml")
print("IFRAMES")
for i in soup.find_all("iframe"):
    print(i.get("src"), i.get("id"), i.get("class"))
print("COOKIE")
for el in soup.find_all(id=re.compile(r"cookie|consent|usercentrics|cmp", re.I)):
    print(el.name, el.get("id"))
print("lazy", len(soup.select("img[data-src], img[data-lazy], img[loading]")))
imgs = soup.find_all("img")
print("imgs", len(imgs))
missing = 0
for img in imgs:
    src = img.get("src") or ""
    if not src or src.startswith("data:"):
        missing += 1
        print("NOSRC", img.get("data-src"), img.get("class"))
print("nosrc", missing)
styles = "".join(s.get_text() or "" for s in soup.find_all("style"))
urls = re.findall(r"url\(([^)]+)\)", styles)
print("css urls", len(urls))
c = Counter()
for raw in urls:
    u = raw.strip().strip("\"'")
    c[u] += 1
for u, n in c.most_common(50):
    print(n, u[:140])
