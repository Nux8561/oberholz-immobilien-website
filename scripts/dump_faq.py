from pathlib import Path
from bs4 import BeautifulSoup

soup = BeautifulSoup(Path("index.html").read_text(encoding="utf-8"), "lxml")
faq = soup.select_one("div.faq")
text = faq.prettify() if faq else ""
Path("analysis/faq-snippet.html").write_text(text[:6000], encoding="utf-8")
print(text[:2500])
