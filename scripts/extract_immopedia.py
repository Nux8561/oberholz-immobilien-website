"""Immopedia: alle Begriffsseiten → public/data/immopedia/<slug>.json + public/data/immopedia/index.json"""
import asyncio, json, re
from playwright.async_api import async_playwright
from _common import ROOT

BASE = "https://oberholz-immobilien.pages.dev"
OUT = ROOT / "public" / "data" / "immopedia"
JS = r"""() => {
  const T = e => (e.innerText || '').replace(/\s+/g, ' ').trim();
  const root = document.querySelector('main') || document.body;
  const h1 = root.querySelector('h1');
  const blocks = [];
  root.querySelectorAll('h2,h3,p,ul,ol,blockquote,table').forEach(e => {
    if (e.closest('header,footer,nav,form,aside,.toc') || e.parentElement.closest('ul,ol,table')) return;
    const t = e.tagName.toLowerCase(), x = T(e);
    if (!x || /^Inhaltsverzeichnis$/.test(x)) return;
    if (t === 'ol' && /Inhaltsverzeichnis/.test(x)) return;
    if (t === 'ul' || t === 'ol') blocks.push({ t, items: [...e.children].map(T).filter(Boolean) });
    else if (t === 'table') blocks.push({ t, rows: [...e.rows].map(r => [...r.cells].map(T)) });
    else blocks.push({ t, text: x });
  });
  // Dubletten (blockquote + gleichlautender Absatz) entfernen, Kontakt-Floskeln am Ende abschneiden
  const out = []; for (const b of blocks) { const prev = out[out.length - 1]; if (prev && prev.text && prev.text === b.text) continue; out.push(b); }
  const cut = out.findIndex(b => b.text && /Gerne helfen wir Ihnen|Ihr Michael Oberholz|Wir helfen Ihnen gerne|Rufen Sie uns an/.test(b.text));
  return { term: h1 ? T(h1) : document.title, blocks: cut > 0 ? out.slice(0, cut) : out };
}"""

async def one(ctx, url, index, sem):
    async with sem:
        slug = re.sub(r"\.html$", "", url.rsplit("/", 1)[1])
        dest = OUT / f"{slug}.json"
        if dest.exists():
            d = json.loads(dest.read_text())
        else:
            pg = await ctx.new_page()
            try:
                await pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                d = await pg.evaluate(JS)
            except Exception as e:
                print("ERR", slug, str(e)[:60]); await pg.close(); return
            await pg.close()
            if not d["blocks"]: return
            dest.write_text(json.dumps(d, ensure_ascii=False))
        first = next((b["text"] for b in d["blocks"] if b.get("t") == "p"), "")
        index.append({"slug": slug, "term": d["term"], "short": first[:220]})
        if len(index) % 100 == 0: print(len(index))

async def main():
    urls = [u for u in json.loads((ROOT / "analysis" / "oberholz-pages" / "uncrawled.json").read_text()) if "/immopedia/" in u]
    index, sem = [], asyncio.Semaphore(8)
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context()
        await ctx.route("**/*.{png,jpg,jpeg,webp,svg,woff,woff2,gif}", lambda r: r.abort())
        await asyncio.gather(*[one(ctx, u, index, sem) for u in urls])
        await b.close()
    index.sort(key=lambda x: x["term"].lower())
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False))
    print("fertig:", len(index))

asyncio.run(main())
