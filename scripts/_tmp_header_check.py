from pathlib import Path
import re

text = Path("index.html").read_text(encoding="utf-8", errors="ignore")
i = text.find("topbar-menu-desktop")
print("index.html pos", i)
if i >= 0:
    print(text[i - 120 : i + 350])
print("nav-fix linked", "oberholz-nav-fix" in text)
for m in re.finditer(r'href=["\']([^"\']*oberholz[^"\']*)["\']', text):
    print("link", m.group(1))
count = 0
for f in Path("public").rglob("*.html"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    if "topbar-menu-desktop" in t and "fixed-top" in t:
        count += 1
print("pages with fixed topbar", count)
j = text.find("navbar-wrapper")
print("navbar-wrapper snippet:", repr(text[j : j + 80]) if j >= 0 else None)
