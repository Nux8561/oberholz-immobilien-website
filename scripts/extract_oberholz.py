"""Strukturierte Inhalte der Oberholz-Seite (Überschriften, Absätze, Listen, Tabellen, Bilder, Links in Reihenfolge)
→ analysis/oberholz-pages/content/<slug>.json. Aufruf: python3 scripts/extract_oberholz.py [pfad …]"""
import asyncio, json, re, sys
from playwright.async_api import async_playwright
from _common import ROOT

BASE = "https://oberholz-immobilien.pages.dev"
OUT = ROOT / "analysis" / "oberholz-pages" / "content"

JS = r"""() => {
  const T = e => (e.innerText || '').replace(/\s+/g, ' ').trim();
  const skip = e => e.closest('header, footer, nav, form, script, style, noscript, .modal, [aria-hidden="true"]');
  const root = document.querySelector('main') || document.body;
  const out = []; const seen = new Set();
  root.querySelectorAll('h1,h2,h3,h4,p,ul,ol,table,img,blockquote,dl,a[href$=".pdf"],details').forEach(e => {
    if (skip(e) || seen.has(e)) return;
    if (e.closest('ul,ol,table,dl,details') && !['UL','OL','TABLE','DL','DETAILS'].includes(e.tagName) && e.tagName !== 'IMG' && !(e.tagName==='A')) { if (e.closest('ul,ol,table,dl,details') !== e) return; }
    const tag = e.tagName.toLowerCase();
    if (tag === 'img') { if (e.naturalWidth > 120) out.push({ t: 'img', src: e.currentSrc || e.src, alt: e.alt, w: e.naturalWidth, h: e.naturalHeight }); return; }
    if (tag === 'a') { out.push({ t: 'pdf', href: e.href, text: T(e) }); return; }
    if (tag === 'ul' || tag === 'ol') { if (e.parentElement.closest('ul,ol')) return; out.push({ t: tag, items: [...e.children].map(T).filter(Boolean) }); e.querySelectorAll('*').forEach(x => seen.add(x)); return; }
    if (tag === 'table') { out.push({ t: 'table', rows: [...e.rows].map(r => [...r.cells].map(T)) }); e.querySelectorAll('*').forEach(x => seen.add(x)); return; }
    if (tag === 'dl') { const it = []; e.querySelectorAll('dt').forEach(dt => it.push([T(dt), T(dt.nextElementSibling || dt)])); out.push({ t: 'dl', items: it }); e.querySelectorAll('*').forEach(x => seen.add(x)); return; }
    if (tag === 'details') { const s = e.querySelector('summary'); out.push({ t: 'qa', q: s ? T(s) : '', a: T(e).replace(s ? T(s) : '', '').trim() }); e.querySelectorAll('*').forEach(x => seen.add(x)); return; }
    const txt = T(e); if (!txt) return;
    out.push({ t: tag, text: txt });
  });
  return { title: document.title, url: location.href, blocks: out };
}"""

async def main():
    paths = sys.argv[1:]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1440, "height": 900})
        for path in paths:
            url = BASE + path
            try:
                await pg.goto(url, wait_until="networkidle", timeout=45000)
                # „Mehr anzeigen“ aufklappen
                await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                d = await pg.evaluate(JS)
            except Exception as e:
                print("ERR", path, str(e)[:100]); continue
            slug = re.sub(r"[^a-z0-9]+", "-", path.lower().replace(".html", "")).strip("-") or "home"
            (OUT / f"{slug}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
            print(slug, len(d["blocks"]))
        await b.close()

asyncio.run(main())
