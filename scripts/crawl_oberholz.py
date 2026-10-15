"""Erfasst die vorbereitete Oberholtz-Seite (oberholz-immobilien.pages.dev): alle internen Seiten (BFS),
Titel, Überschriften, Text, Links, Formulare und Full-Page-Screenshots → analysis/oberholz-pages/"""
import asyncio, json, re
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from _common import ROOT

BASE = "https://oberholz-immobilien.pages.dev/"
OUT = ROOT / "analysis" / "oberholz-pages"
LIMIT = 120

JS = r"""() => {
  const txt = e => (e.innerText || '').trim().replace(/\s+/g, ' ');
  return {
    title: document.title,
    h: [...document.querySelectorAll('h1,h2,h3')].map(e => e.tagName + ': ' + txt(e)).slice(0, 80),
    links: [...document.querySelectorAll('a[href]')].map(a => ({ href: a.href, text: txt(a).slice(0, 80) })),
    buttons: [...document.querySelectorAll('button')].map(b => txt(b).slice(0, 60)).filter(Boolean).slice(0, 60),
    forms: [...document.querySelectorAll('form')].map(f => ({ id: f.id, action: f.getAttribute('action'), fields: [...f.querySelectorAll('input,select,textarea')].map(i => (i.name || i.id || i.type) + ':' + (i.placeholder || '')) })),
    text: txt(document.body).slice(0, 12000),
    height: document.documentElement.scrollHeight,
  };
}"""

def norm(u):
    p = urlparse(u)
    return f"{p.scheme}://{p.netloc}{p.path}".rstrip("/") or u

async def main():
    seen, queue, pages = set(), [BASE], {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1440, "height": 900}, locale="de-DE")
        page = await ctx.new_page()
        while queue and len(pages) < LIMIT:
            url = queue.pop(0); key = norm(url)
            if key in seen: continue
            seen.add(key)
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)
                await page.wait_for_timeout(600)
                d = await page.evaluate(JS)
            except Exception as e:
                pages[key] = {"error": str(e)[:200]}; continue
            pages[key] = d
            slug = re.sub(r"[^a-z0-9]+", "-", urlparse(key).path.lower()).strip("-") or "home"
            try:
                await page.screenshot(path=str(OUT / "shots" / f"{slug}.png"), full_page=True)
            except Exception:
                pass
            for l in d["links"]:
                h = l["href"]
                if urlparse(h).netloc == urlparse(BASE).netloc and not re.search(r"\.(pdf|jpg|png|webp|zip)$", h, re.I):
                    if norm(h) not in seen: queue.append(h)
            print(len(pages), key, d["title"][:60], d["height"])
        await b.close()
    (OUT / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=1))

asyncio.run(main())
