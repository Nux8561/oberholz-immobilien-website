import re
from pathlib import Path

root = Path("public")
have = {"/" + path.relative_to(root).as_posix() for path in root.rglob("*.html")}
print("have", len(have), flush=True)
files = list(root.glob("*.html"))
for folder in ("leistungen", "kontakt", "service", "ratgeber", "ueber-uns", "immobilien"):
    folder_path = root / folder
    if folder_path.exists():
        files.extend(list(folder_path.rglob("*.html"))[:40])
region = next((root / "regionen").glob("*.html"), None)
article = next((root / "immopedia").rglob("*.html"), None)
if region:
    files.append(region)
if article:
    files.append(article)
missing: dict[str, int] = {}
pattern = re.compile(r"""href=["'](/[^"']+\.html)""")
for path in files:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for href in pattern.findall(text):
        href = href.split("#")[0].split("?")[0]
        if href not in have:
            missing[href] = missing.get(href, 0) + 1
print("scanned", len(files), "missing", len(missing), flush=True)
for key, count in sorted(missing.items(), key=lambda item: -item[1])[:40]:
    print(count, key)
