"""Find internal HTML links that are not mirrored yet."""
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

root = Path("public")
have = set()
for path in root.rglob("*.html"):
    rel = "/" + path.relative_to(root).as_posix()
    have.add(rel)

missing = {}
pattern = re.compile(r"""href=["']([^"']+\.html)""")
for path in root.rglob("*.html"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    base = "https://www.immobilien-experten.de/" + path.relative_to(root).as_posix()
    for raw in pattern.findall(text):
        if raw.startswith(("mailto:", "tel:", "javascript:")):
            continue
        if raw.startswith("http") and "immobilien-experten.de" not in raw:
            continue
        if raw.startswith("http"):
            target = urlparse(raw).path
        elif raw.startswith("/"):
            target = raw.split("#")[0].split("?")[0]
        else:
            target = urlparse(unquote(raw.split("#")[0].split("?")[0])).path
            parent = "/" + str(path.parent.relative_to(root)).replace("\\", "/")
            if parent == "/.":
                parent = ""
            target = (parent + "/" + target.lstrip("./")).replace("//", "/")
            while "/./" in target:
                target = target.replace("/./", "/")
        target = unquote(target.split("#")[0].split("?")[0])
        if not target.endswith(".html"):
            continue
        if target not in have:
            missing[target] = missing.get(target, 0) + 1

print("have", len(have))
print("missing", len(missing))
for key, count in sorted(missing.items(), key=lambda item: -item[1])[:40]:
    print(count, key)
