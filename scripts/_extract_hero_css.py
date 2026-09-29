from pathlib import Path
import re

detail = Path("public/immobilien/bochum/attraktive-kapitalanlage-faktor-13-9-vermietetes-dreiparteienhaus-in-bochum-lang-170744873.html").read_text(encoding="utf-8")
# pull all CSS text
css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", detail, re.S | re.I))
# find rules containing immo-detail
for m in re.finditer(r"[^{}]*immo-detail[^{]*\{[^{}]*\}", css):
    print(m.group(0)[:500])
    print("---")
