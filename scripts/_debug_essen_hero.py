from pathlib import Path
import re

p = Path("public/immobilien/essen/geraumiges-sanierungsbedurftiges-reihenendhaus-in-ruhiger-lage-in-essen-kupferdr-170212293.html")
h = p.read_text(encoding="utf-8")

# Extract hero block
m = re.search(r'<div class="immo-detail-hero">.*?</div>\s*</div>\s*<div class="col-12 col-md-4', h, re.S)
if m:
    Path("assets/oberholz/_essen_hero_dump.html").write_text(m.group(0)[:4000], encoding="utf-8")
    print("dumped", len(m.group(0)))
else:
    print("no match")
    i = h.find('class="immo-detail-hero"')
    print(h[i:i+2500])

# Find conflicting CSS for img / gallery
css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", h, re.S|re.I))
for pat in ["gallery-trigger", "immo-detail-hero", "picture", "object-fit", ".ratio"]:
    hits = [x.strip()[:200] for x in re.findall(rf"[^{{}}]*{re.escape(pat)}[^{{}}]*\{{[^{{}}]*\}}", css, re.I)]
    print(pat, "rules", len(hits))
    for x in hits[:5]:
        print(" ", x)

# Count img tags pointing to hero
print("hero srcs", re.findall(r'/media/object-hero[^"\s]+', h))
