from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "assets/oberholz/_is24_expose_sample.html").read_text(encoding="utf-8")

# relative listing image paths
rels = list(dict.fromkeys(re.findall(r"(?:https:)?(?://pictures\.immobilienscout24\.de)?(/listings/[a-f0-9\-]+-\d+\.(?:jpg|jpeg|png)[^\"'\s<>]*)", html, re.I)))
print("rels", len(rels))
for u in rels[:20]:
    print(u[:180])

# also bare filenames
bare = list(dict.fromkeys(re.findall(r"/listings/[a-f0-9\-]+-\d+\.(?:jpg|jpeg|png)", html, re.I)))
print("bare", len(bare))
for u in bare[:20]:
    print(u)

# try to get description text
def section(label):
    m = re.search(rf"{label}</h4>\s*<p[^>]*>(.*?)</p>", html, re.S | re.I)
    if not m:
        m = re.search(rf"{label}.*?<p[^>]*>(.*?)</p>", html, re.S | re.I)
    if m:
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        text = re.sub(r"\s+", " ", text).strip()
        print(label, ":", text[:300])
    else:
        print(label, ": NOT FOUND")

for lab in ["Objektbeschreibung", "Ausstattung", "Lage", "Sonstiges"]:
    section(lab)

# data-src absolute?
datas = list(dict.fromkeys(re.findall(r'data-src="([^"]+)"', html)))
print("data-src", len(datas))
for d in datas[:15]:
    print(d[:160])
