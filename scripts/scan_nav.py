from pathlib import Path
from bs4 import BeautifulSoup

soup = BeautifulSoup(Path("index.html").read_text(encoding="utf-8"), "lxml")
faq = soup.select("[data-bs-toggle='collapse'], .accordion-button, .faq")
print("faq toggles", len(faq))
for el in faq[:12]:
    print(el.name, el.get("class"), (el.get_text(" ", strip=True) or "")[:90])

menus = soup.select("nav .nav-item.dropdown > a, nav .nav-link")
print("---NAV---")
for el in menus[:20]:
    print((el.get_text(" ", strip=True) or "")[:40], el.get("href"))
