from pathlib import Path
import re

text = Path("index.html").read_text(encoding="utf-8")
Path("scripts/_listings_behavior.txt").write_text("", encoding="utf-8")
# Find JS related to immo cards
matches = []
for m in re.finditer(r".{0,80}immo-(?:card|img)[a-zA-Z-]*.{0,120}", text):
    s = m.group(0).replace("\n", " ")
    if "function" in s or "addEventListener" in s or "mouse" in s or "querySelector" in s:
        matches.append(s)
Path("scripts/_listings_behavior.txt").write_text("\n\n".join(matches[:40]), encoding="utf-8")
print("matches", len(matches))
sec_start = text.rfind("<section", 0, text.find("Aktuelle Immobilien aus unserer Vermittlung"))
sec_end = text.find("</section>", text.find("Aktuelle Immobilien aus unserer Vermittlung"))
Path("scripts/_listings_full.txt").write_text(text[sec_start:sec_end + 10], encoding="utf-8")
print("section", sec_end - sec_start)
print("cards", text[sec_start:sec_end].count("immo-card"))
