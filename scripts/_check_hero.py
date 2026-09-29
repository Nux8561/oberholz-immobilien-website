from pathlib import Path
import re

oid = "170744873"
media = Path("public/media")
for folder in ["object-hero-780", "object-thumb-780", "object-thumbnail-780", "object-zoom-780"]:
    p = media / folder / f"{oid}_000.jpg"
    p1 = media / folder / f"{oid}_001.jpg"
    print(folder, "000", p.exists(), p.stat().st_size if p.exists() else 0, "001", p1.exists(), p1.stat().st_size if p1.exists() else 0)

detail = Path("public/immobilien/bochum/attraktive-kapitalanlage-faktor-13-9-vermietetes-dreiparteienhaus-in-bochum-lang-170744873.html")
html = detail.read_text(encoding="utf-8")
# find hero img tag
m = re.search(r'object-hero-780/[^"\s]+', html)
print("hero ref", m.group(0) if m else None)
# check if old CSS forces absolute on all picture/img in main
print("immo-detail count", html.count("immo-detail"))
print("ratio-16x9", html.count("ratio-16x9"))
# extract hero block
i = html.find("ratio-16x9")
print(html[i-200:i+400] if i>0 else "no ratio")

# count secondary on homepage
index = Path("index.html").read_text(encoding="utf-8")
print("homepage secondary tpl", index.count("immo-img-secondary-tpl"))
print("homepage internal immobilien", len(re.findall(r'href="/immobilien/[^"]+"', index)))
