"""Mega-Menüs, Objektarten-Dropdown, Mobile-Menü, Slider-Timing, Hero-Teaser-Position erfassen."""
import asyncio, json
from playwright.async_api import async_playwright
from _common import open_original, ANA, REF

MENU_JS = r"""
(root) => {
  const out = [];
  const walk = (el, d) => {
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    if (cs.display==='none' || cs.visibility==='hidden' || r.width===0) return;
    const t = [...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
    if (t || ['a','button','img','h2','h3','h4','p','ul','svg'].includes(el.tagName.toLowerCase()) || d<4)
      out.push({d, tag: el.tagName.toLowerCase(), t: t.slice(0,90), r:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)],
        fs: cs.fontSize, fw: cs.fontWeight, lh: cs.lineHeight, ff: cs.fontFamily.split(',')[0], c: cs.color, bg: cs.backgroundColor,
        pad: cs.padding, bb: cs.borderBottom, tt: cs.textTransform, ls: cs.letterSpacing, href: el.getAttribute('href')||undefined});
    if (el.tagName.toLowerCase()!=='svg') for (const c of el.children) walk(c, d+1);
  };
  walk(root, 0); return out;
}
"""

async def main():
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await open_original(b, 1440, 900)
        # Hero-Teaser Sichtbarkeit / Transform
        res['teasers'] = await page.evaluate("""() => [...document.querySelectorAll('article')].slice(0,3).map(a=>{const cs=getComputedStyle(a); const r=a.getBoundingClientRect(); return {r:[r.x,r.y+scrollY,r.width,r.height], op:cs.opacity, tr:cs.transform, bg:cs.backgroundColor, sh:cs.boxShadow, pad:cs.padding, parentOp:getComputedStyle(a.parentElement).opacity}})""")
        # Pseudo-Element Linie in Section-Headern
        res['lines'] = await page.evaluate("""() => [...document.querySelectorAll('main header')].slice(0,6).map(h=>{const o={}; for (const pe of ['::before','::after']) {const cs=getComputedStyle(h,pe); if(cs.content!=='none') o[pe]={content:cs.content,w:cs.width,h:cs.height,bg:cs.backgroundColor,top:cs.top,left:cs.left,pos:cs.position,margin:cs.margin,display:cs.display}}; const cs=getComputedStyle(h); o.pad=cs.padding; o.display=cs.display; return o;})""")
        # Slider: aktiver Index über Zeit
        res['slider'] = await page.evaluate("""async () => { const ul=document.querySelector('main ul'); const tr=[]; for(let i=0;i<14;i++){ tr.push({t:i*1000, transform:getComputedStyle(ul).transform, trans:getComputedStyle(ul).transition}); await new Promise(r=>setTimeout(r,1000)); } return tr; }""")
        # Fortschrittsbalken
        res['progress'] = await page.evaluate("""() => { const vids=document.querySelectorAll('main video'); return [...vids].map(v=>({poster:!!v.poster, dur:v.duration, loop:v.loop, muted:v.muted, autoplay:v.autoplay})) }""")
        await page.screenshot(path=str(REF / "hero_viewport_1440.png"))
        # Objektarten-Dropdown
        await page.click("button[aria-label='Dropdown-Menü für Objektarten']")
        await page.wait_for_timeout(600)
        await page.screenshot(path=str(REF / "dropdown_open_1440.png"), clip={"x":600,"y":150,"width":840,"height":600})
        res['dropdown'] = await page.evaluate("""() => { const l=[...document.querySelectorAll('[role=listbox],[role=menu],[role=option],ul')].filter(e=>e.getBoundingClientRect().y>290 && e.getBoundingClientRect().y<700 && e.offsetParent); return l.slice(0,3).map(e=>({tag:e.tagName, role:e.getAttribute('role'), text:e.innerText.slice(0,400), r:JSON.stringify(e.getBoundingClientRect())})) }""")
        await page.keyboard.press("Escape"); await page.mouse.click(300, 600); await page.wait_for_timeout(400)
        # Mega-Menüs
        res['menus'] = {}
        labels = ["Kaufen & Mieten","Immobilie verkaufen","Immobilienmakler","Commercial","Unternehmen"]
        for i, lab in enumerate(labels):
            await page.evaluate("window.scrollTo(0,0)")
            await page.hover(f"nav a:has-text('{lab}')")
            await page.wait_for_timeout(900)
            await page.screenshot(path=str(REF / f"megamenu_{i}_1440.png"))
            info = await page.evaluate("""() => { const c=[...document.querySelectorAll('header div, header section, div[class*=flyout], div[class*=Flyout]')].filter(e=>{const r=e.getBoundingClientRect(); return r.y>=100 && r.height>150 && r.width>600 && getComputedStyle(e).visibility!=='hidden' && getComputedStyle(e).display!=='none'}); c.sort((a,b)=>b.getBoundingClientRect().height-a.getBoundingClientRect().height); return c.length? {cls:c[0].className, r:JSON.stringify(c[0].getBoundingClientRect()), bg:getComputedStyle(c[0]).backgroundColor, sh:getComputedStyle(c[0]).boxShadow, tr:getComputedStyle(c[0]).transition}: null }""")
            items = None
            if info:
                items = await page.evaluate(f"""() => {{ const el=[...document.querySelectorAll('*')].find(e=>e.className==={json.dumps(info['cls'])}); return ({MENU_JS})(el) }}""")
            res['menus'][lab] = {'container': info, 'items': items}
            await page.mouse.move(700, 800); await page.wait_for_timeout(500)
        await page.close()
        # Mobile-Menü
        mp = await open_original(b, 390, 844, mobile=True)
        await mp.screenshot(path=str(REF / "mobile_top_390.png"))
        (ANA / "interactions.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
        await mp.mouse.click(28, 28)
        await mp.wait_for_timeout(900)
        await mp.screenshot(path=str(REF / "mobile_menu_open_390.png"))
        res['mobile_menu'] = await mp.evaluate(f"""() => {{ const d=[...document.querySelectorAll('dialog, [role=dialog], nav, div')].filter(e=>{{const r=e.getBoundingClientRect(); return r.width>=380 && r.height>500 && getComputedStyle(e).position.match(/fixed|absolute/)}}); return d.length? ({MENU_JS})(d[0]).slice(0,120) : null }}""")
        # erstes Untermenü auf Mobile öffnen
        try:
            await mp.click("text=Kaufen & Mieten >> visible=true", timeout=3000); await mp.wait_for_timeout(800)
            await mp.screenshot(path=str(REF / "mobile_menu_sub_390.png"))
        except Exception as e:
            res['mobile_sub_err'] = str(e)[:200]
        await b.close()
    (ANA / "interactions.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print("ok")

asyncio.run(main())
