from pathlib import Path

t = Path("assets/oberholz/_sample_main.html").read_text(encoding="utf-8")
# write first 12000 chars of gallery area starting at immo-detail-hero
i = t.find("immo-detail-hero")
Path("assets/oberholz/_sample_hero_block.html").write_text(t[i : i + 12000], encoding="utf-8")
print("wrote", 12000, "from", i)
# also find style definition if inline near end of head - already in page
# count class occurrences
for c in ["immo-detail-hero", "immo-detail-hero-img", "immo-detail-thumbgrid", "immo-detail-thumbcell", "immo-detail-hero-overlay", "immo-detail-hero-content"]:
    print(c, t.count(c))
