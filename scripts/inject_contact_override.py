#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = '<script src="/theme/oberholz-contact-override.js" defer></script>'

files = [ROOT / "index.html"]
for folder in [
    ROOT / "public",
    ROOT / "public" / "leistungen",
    ROOT / "public" / "ueber-uns",
    ROOT / "public" / "service",
    ROOT / "public" / "ratgeber",
    ROOT / "public" / "kontakt",
]:
    files.extend(folder.glob("*.html"))

changed = 0
for path in sorted(set(files)):
    if not path.is_file():
        continue
    html = path.read_text(encoding="utf-8", errors="replace")
    if "cw-trigger" not in html and "cwTriggerClick" not in html:
        continue
    if "oberholz-contact-override.js" in html:
        continue
    if "</body>" in html:
        html2 = html.replace("</body>", SCRIPT + "\n</body>", 1)
    else:
        html2 = html + SCRIPT
    path.write_text(html2, encoding="utf-8")
    changed += 1
    print("updated", path.relative_to(ROOT))
print("Done", changed)
