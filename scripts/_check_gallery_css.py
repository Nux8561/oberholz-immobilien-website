from pathlib import Path
import re

detail = Path("public/immobilien/bochum/attraktive-kapitalanlage-faktor-13-9-vermietetes-dreiparteienhaus-in-bochum-lang-170744873.html").read_text(encoding="utf-8")
# find style blocks mentioning gallery or immo-detail or img
styles = re.findall(r"<style[^>]*>(.*?)</style>", detail, re.S | re.I)
print("style blocks", len(styles))
for i, s in enumerate(styles):
    if any(k in s.lower() for k in ["gallery", "immo-detail", "object-fit", "ratio", "hero", "thumb"]):
        print("--- style", i, "len", len(s))
        # print matching lines
        for line in s.split("}"):
            low = line.lower()
            if any(k in low for k in ["gallery", "immo-detail", "hero", "thumb", ".immo-img"]):
                print(line[:300].strip() + "}")

# Also check original main gallery structure start
orig = Path("assets/oberholz/_sample_main.html")
if orig.exists():
    t = orig.read_text(encoding="utf-8")
    # find first object-hero usage context
    i = t.find("object-hero-780")
    print("ORIG HERO CTX:\n", t[max(0,i-600):i+500])
