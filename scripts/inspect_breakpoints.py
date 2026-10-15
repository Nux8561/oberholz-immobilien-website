"""Misst Layoutwechsel über viele Breiten: Header-Höhe, Hero-Grid, Teaser, Städte-Grid, Galerie, Footer."""
import asyncio, json, sys
from playwright.async_api import async_playwright
from _common import open_original, ANA

WIDTHS = [int(x) for x in sys.argv[1:]] or [320,360,375,390,430,480,600,767,768,769,900,1023,1024,1025,1200,1279,1280,1366,1440,1600,1920]

JS = r"""() => {
 const q = s => document.querySelector(s); const R = el => { if(!el) return null; const r=el.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.y+scrollY),Math.round(r.width),Math.round(r.height)] };
 const main = q('main'); const secs=[...main.children];
 const cs = el => el ? getComputedStyle(el) : null;
 const art = [...document.querySelectorAll('main article')];
 const h = q('header'); const nav = q('header nav');
 const title = q('main section p'); const input = q('main input[placeholder]');
 const carousel = q('main ul'); const teaserWrap = art[0]?.parentElement?.parentElement;
 const cityGrid = art[6]?.parentElement;
 const gal = [...document.querySelectorAll('main section button')].filter(b=>b.querySelector('img')).slice(0,6).map(R);
 const intro = [...document.querySelectorAll('main header')][1];
 return { header: R(h), navVisible: nav ? cs(nav).display!=='none' && nav.getBoundingClientRect().width>0 : false, nav: R(nav),
   title: R(title), titleFs: cs(title).fontSize, input: R(input), inputFs: cs(input).fontSize, carousel: R(carousel),
   teasers: art.slice(0,3).map(R), teaserOpacity: teaserWrap? cs(teaserWrap).opacity:null, cities: art.slice(3,9).map(R), gallery: gal,
   introBefore: intro? cs(intro,'::before').height : null, introH: R(intro?.querySelector('h1,h2')), introHfs: cs(intro?.querySelector('h1,h2'))?.fontSize,
   footer: R(q('footer')), footerTitleFs: cs(q('footer p'))?.fontSize, scrollH: document.documentElement.scrollHeight };
}"""

async def one(b, w):
    for attempt in range(3):
        try:
            page = await open_original(b, w, 900, mobile=w < 768)
            d = await page.evaluate(JS); await page.context.close(); return w, d
        except Exception as e:
            print('retry', w, str(e)[:80])
    return w, None

async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in WIDTHS:
            w, d = await one(b, w)
            if d: out[w] = d
        await b.close()
    prev = json.loads((ANA/"breakpoints.json").read_text()) if (ANA/"breakpoints.json").exists() else {}
    prev.update({str(k): v for k, v in out.items()})
    (ANA / "breakpoints.json").write_text(json.dumps(prev, indent=1))
    for w in sorted(out): d=out[w]; print(w, 'hdr', d['header'][3], 'nav', d['navVisible'], 'title', d['title'], d['titleFs'], 'input', d['input'], 'car', d['carousel'], 'teas', d['teasers'][0], d['teaserOpacity'], 'city0', d['cities'][0], 'city1', d['cities'][1], 'gal', d['gallery'][:3], 'introLine', d['introBefore'], d['introH'], d['introHfs'], 'H', d['scrollH'])

asyncio.run(main())
