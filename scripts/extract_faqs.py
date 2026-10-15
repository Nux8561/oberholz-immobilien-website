"""FAQ-Akkordeons (Frage + versteckte Antwort) aller Oberholz-Inhaltsseiten → analysis/oberholz-pages/faqs.json"""
import asyncio, json, re
from playwright.async_api import async_playwright
from _common import ROOT

BASE = "https://oberholz-immobilien.pages.dev"
JS = r"""() => {
  const T = e => (e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '');
  const out = [];
  document.querySelectorAll('.accordion-item, details, [class*=faq] [class*=item]').forEach(it => {
    const q = it.querySelector('.accordion-button, summary, h3, button');
    const a = it.querySelector('.accordion-body, .accordion-collapse, [class*=answer], [class*=content], p');
    const qt = T(q), at = T(a);
    if (qt && at && qt !== at && !out.some(x => x.q === qt)) out.push({ q: qt, a: at.replace(qt, '').trim() });
  });
  return out;
}"""

async def main():
    paths = (ROOT / "analysis" / "oberholz-pages" / "content").glob("*.json")
    slugs = [p.stem for p in paths]
    pages = json.loads((ROOT / "analysis" / "oberholz-pages" / "pages.json").read_text())
    urls = {}
    for k in pages:
        s = re.sub(r"[^a-z0-9]+", "-", k.replace(BASE, "").lower().replace(".html", "")).strip("-") or "home"
        if s in slugs and "immopedia" not in s and not s.startswith("immobilien-"): urls[s] = k
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for s, u in sorted(urls.items()):
            await pg.goto(u, wait_until="domcontentloaded", timeout=45000)
            f = await pg.evaluate(JS)
            if f: res[s] = f; print(s, len(f))
        await b.close()
    (ROOT / "analysis" / "oberholz-pages" / "faqs.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))

asyncio.run(main())
