import re
from pathlib import Path

text = Path("public/immobilien.html").read_text(encoding="utf-8", errors="ignore")
hrefs = re.findall(r"""href=["']([^"']*immobilien-experten\.de[^"']*)["']""", text)
print("hrefs", len(hrefs))
for href in sorted(set(hrefs)):
    print(href[:180])
print("---meta---")
metas = re.findall(r"""content=["']([^"']*immobilien-experten\.de[^"']*)["']""", text)
for meta in sorted(set(metas))[:15]:
    print(meta[:180])
