from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

url = "https://portal.immobilienscout24.de/expose/82828525/170744873/1/1"
req = urllib.request.Request(url, headers=UA)
html = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
(ROOT / "assets/oberholz/_is24_expose_sample.html").write_text(html, encoding="utf-8")
print("html", len(html))

imgs = list(dict.fromkeys(re.findall(r"https://pictures\.immobilienscout24\.de/[^\"'\s<>]+", html)))
print("unique picture urls", len(imgs))
for u in imgs[:30]:
    print(u[:160])

# also look for relative/resized patterns
for pat in [r"/listings/[a-f0-9\-]+-\d+\.(?:jpg|jpeg|png)", r"ORIG/resize", r"data-src="]:
    print(pat, len(re.findall(pat, html)))

# description chunks
for label in ["Objektbeschreibung", "Ausstattung", "Lage", "Sonstiges"]:
    i = html.find(label)
    print(label, "at", i)
