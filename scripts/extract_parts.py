from pathlib import Path
from bs4 import BeautifulSoup

soup = BeautifulSoup(Path("analysis/rendered.html").read_text(encoding="utf-8"), "lxml")
iwf = soup.select_one("#iwf")
Path("analysis/iwf.html").write_text(iwf.prettify() if iwf else "MISSING", encoding="utf-8")
print("iwf", "yes" if iwf else "no", "len", len(iwf.prettify()) if iwf else 0)
header = soup.find("header")
Path("analysis/header.html").write_text(header.prettify()[:20000] if header else "MISSING", encoding="utf-8")
print("header", len(header.prettify()) if header else 0)
footer = soup.find("footer")
print("footer", len(footer.prettify()) if footer else 0)
print("main sections", [(s.get("class"), s.get("id")) for s in soup.select("main > section, main > div")])
