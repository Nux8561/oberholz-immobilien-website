"""Wählt freie Ersatzfonts per Breitenvergleich: misst Referenz-Strings in Kandidaten-Fonts (Google Fonts)
und vergleicht mit den im Original gemessenen Breiten (EV Head VF / EV Text VF sind proprietär)."""
import asyncio, json
from playwright.async_api import async_playwright
from _common import ANA

# (text, px, letterSpacing, uppercase, referenzbreite) – gemessen aus dom_1440.json
TEXT_REF = [("Kaufen & Mieten",16,0.48,False,121),("Immobilie verkaufen",16,0.48,False,149),("Immobilienmakler",16,0.48,False,131),
            ("Commercial",16,0.48,False,89),("Unternehmen",16,0.48,False,101),("Anmelden",16,0.48,False,74.5),("Standorte",16,0.48,False,74.2),
            ("Immobilie verkaufen",12,2,True,167),("Immobilie kaufen",12,2,True,138),("Makler werden",12,2,True,125),("Preis auf Anfrage",12,2,True,147),
            ("Jetzt erfolgreich verkaufen",16,0.48,False,199.6),("Hier informieren",16,0.48,False,119.75),("Haus kaufen in Hamburg",16,0.48,False,178),("Haus kaufen in Berlin",16,0.48,False,153.3)]
HEAD_REF = [("Berlin, Deutschland",24,0,False,214),("Argyronisos Greece",24,0,False,218),("Köln, Deutschland",24,0,False,200),("Frankfurt, Deutschland",24,0,False,255),
            ("Albufeira, Portugal",24,0,False,206),("Traumimmobilie kaufen",16,0,False,172),("Erfolgreich verkaufen",16,0,False,157),("Immobilienberater werden",16,0,False,193),
            ("Kontaktieren Sie uns",28,0,False,265)]
TEXT_C = ["Hanken Grotesk","Inter","Work Sans","Instrument Sans","Figtree","Schibsted Grotesk","Public Sans","DM Sans","Albert Sans","Geist","Inter Tight","Manrope","Onest","Golos Text"]
HEAD_C = ["Newsreader","Lora","Crimson Pro","Source Serif 4","Literata","Gelasio","Libre Caslon Text","EB Garamond","Spectral","Alegreya","Cormorant Garamond","Fraunces","Petrona","Brygada 1918","Besley","Young Serif","Gloock","Rasa","Piazzolla","Vollkorn","Merriweather","Noticia Text"]

async def measure(page, fam, refs, weights):
    res = {}
    for w in weights:
        widths = await page.evaluate("""([fam,w,refs]) => refs.map(([t,px,ls,up]) => { const s=document.createElement('span'); s.style.cssText=`font-family:'${fam}';font-weight:${w};font-size:${px}px;letter-spacing:${ls}px;white-space:nowrap;position:absolute;${up?'text-transform:uppercase;':''}`; s.textContent=t; document.body.appendChild(s); const x=s.getBoundingClientRect().width; s.remove(); return x;})""", [fam, w, [r[:4] for r in refs]])
        errs = [ (m - r[4]) / r[4] for m, r in zip(widths, refs)]
        res[w] = {"mean_err_pct": round(100*sum(errs)/len(errs),2), "abs_err_pct": round(100*sum(abs(e) for e in errs)/len(errs),2)}
    return res

async def main():
    fams = TEXT_C + HEAD_C
    q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;600;700" for f in fams)
    html = f"<html><head><link rel=stylesheet href='https://fonts.googleapis.com/css2?{q}&display=block'></head><body>" + "".join(f"<span style=\"font-family:'{f}';font-weight:{w}\">Aa</span>" for f in fams for w in (400,500,600,700)) + "</body></html>"
    out = {"text": {}, "head": {}}
    async with async_playwright() as p:
        b = await p.chromium.launch(); page = await b.new_page()
        await page.set_content(html); await page.wait_for_timeout(3000); await page.evaluate("document.fonts.ready")
        for f in TEXT_C: out["text"][f] = await measure(page, f, TEXT_REF, (400,500))
        for f in HEAD_C: out["head"][f] = await measure(page, f, HEAD_REF, (400,500,600,700))
        await b.close()
    (ANA / "font_candidates.json").write_text(json.dumps(out, indent=1))
    for k in out:
        rows = sorted(((v2["abs_err_pct"], f, w, v2["mean_err_pct"]) for f, v in out[k].items() for w, v2 in v.items()))
        print(k); [print(f"  {f:22s} w{w}  abs {a:5.2f}%  mean {m:+.2f}%") for a, f, w, m in rows[:10]]

asyncio.run(main())
