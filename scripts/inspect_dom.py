"""Rendert die Seite und speichert DOM-Baum (Sections), Geometrie, Computed Styles, Fonts, CSS-Variablen.
Aufruf: python3 scripts/inspect_dom.py [breite höhe]"""
import asyncio, json, sys
from playwright.async_api import async_playwright
from _common import open_original, ANA, REF

JS = r"""
() => {
  const PROPS = ['font-family','font-size','font-weight','line-height','letter-spacing','text-transform',
    'color','background-color','background-image','width','height','max-width','min-height','margin','padding','gap',
    'display','position','grid-template-columns','flex-direction','align-items','justify-content','border','border-bottom',
    'border-radius','box-shadow','object-fit','object-position','opacity','transform','transition','animation','z-index','aspect-ratio','text-decoration'];
  const sy = window.scrollY;
  const rect = el => { const r = el.getBoundingClientRect(); return {x:Math.round(r.x), y:Math.round(r.y+sy), w:Math.round(r.width), h:Math.round(r.height)}; };
  const style = el => { const cs = getComputedStyle(el); const o={}; for (const p of PROPS){ const v=cs.getPropertyValue(p); if(v && v!=='none' && v!=='normal' && v!=='auto' && v!=='0px' && v!=='rgba(0, 0, 0, 0)') o[p]=v;} return o; };
  const vis = el => { const cs=getComputedStyle(el); const r=el.getBoundingClientRect(); return cs.display!=='none' && cs.visibility!=='hidden' && r.width>0 && r.height>0; };
  const describe = (el, depth, maxDepth) => {
    if (!vis(el) && !['svg'].includes(el.tagName.toLowerCase())) return null;
    const tag = el.tagName.toLowerCase();
    const d = {tag, cls: (el.getAttribute('class')||'').slice(0,120), id: el.id||undefined, r: rect(el)};
    const direct = [...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
    if (direct) d.text = direct.slice(0,200);
    for (const a of ['role','aria-label','href','src','alt','placeholder','type','data-testid','srcset']) { const v=el.getAttribute(a); if(v) d[a]= a==='srcset'? v.slice(0,300): v.slice(0,200);}
    if (tag==='img') { d.currentSrc = el.currentSrc; d.natural=[el.naturalWidth, el.naturalHeight]; }
    if (['h1','h2','h3','h4','h5','p','a','button','span','input','img','label','li','section','header','footer','nav','picture','video','div'].includes(tag)) d.s = style(el);
    if (tag==='svg') return d;
    if (depth < maxDepth) { const ch=[...el.children].map(c=>describe(c, depth+1, maxDepth)).filter(Boolean); if (ch.length) d.c=ch; }
    return d;
  };
  const header = document.querySelector('header');
  const main = document.querySelector('main') || document.body;
  const footer = document.querySelector('footer');
  const sections = [...main.children].filter(vis).map(el => describe(el, 0, 18));
  // Fonts
  const fonts = [...document.fonts].map(f => ({family:f.family, weight:f.weight, style:f.style, status:f.status}));
  const faces = [];
  for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) { if (r.type===5) faces.push(r.cssText.slice(0,400)); } } catch(e){} }
  const rootVars = {}; const rcs = getComputedStyle(document.documentElement);
  for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) { if (r.selectorText && /:root|html/.test(r.selectorText)) { for (const p of r.style) if (p.startsWith('--')) rootVars[p]=rcs.getPropertyValue(p).trim(); } } } catch(e){} }
  return {
    url: location.href, viewport:[innerWidth, innerHeight], scrollHeight: document.documentElement.scrollHeight,
    body: style(document.body),
    header: header ? describe(header,0,20) : null,
    sections, footer: footer ? describe(footer,0,20) : null,
    fonts, faces, rootVars,
  };
}
"""

async def main():
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
    h = int(sys.argv[2]) if len(sys.argv) > 2 else 900
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await open_original(b, w, h, mobile=w < 768)
        data = await page.evaluate(JS)
        (ANA / f"dom_{w}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
        await page.screenshot(path=str(REF / f"full_{w}.png"), full_page=True)
        print("saved", w, "scrollHeight", data["scrollHeight"], "sections", len(data["sections"]))
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
