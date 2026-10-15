"""Prerendering + Sitemap für Suchmaschinen. Aufruf: npm run build:seo  (vite build → dieses Skript)

Startet `vite preview`, ruft alle internen Seiten auf (Breitensuche ab „/“) und speichert das fertig gerenderte HTML
(inkl. Titel, Meta-Description, Canonical, Open Graph und JSON-LD) als dist/<pfad>/index.html.
Erzeugt außerdem dist/sitemap.xml und dist/robots.txt. Option --immopedia rendert zusätzlich alle Lexikon-Einträge.
"""
import asyncio, datetime, json, re, shutil, subprocess, sys, time, urllib.request
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PORT = 4174
BASE = f"http://localhost:{PORT}"
SITE_URL = re.search(r"SITE_URL = '([^']+)'", (ROOT / "src/data/routes.ts").read_text()).group(1)
WITH_IMMOPEDIA = "--immopedia" in sys.argv
SKIP = ("/downloads/", "/assets/", "/data/")
NOINDEX = ("/mein-bereich", "/cookie-hinweise")


def wait_for_server():
    for _ in range(60):
        try:
            urllib.request.urlopen(BASE, timeout=1)
            return
        except Exception:
            time.sleep(0.5)
    raise SystemExit("vite preview startet nicht")


async def render_all():
    routes, queue, seen = [], ["/"], {"/"}
    imm = json.loads((ROOT / "public/data/immopedia/index.json").read_text())
    imm_routes = [f"/immopedia/{e['slug']}" for e in imm]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(locale="de-DE", viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()
        async def render(path):
            await page.goto(BASE + path, wait_until="networkidle")
            await page.wait_for_timeout(120)
            html = await page.content()
            out = DIST / path.strip("/") / "index.html" if path != "/" else DIST / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            return await page.eval_on_selector_all("a[href^='/']", "els => els.map(e => e.getAttribute('href'))")
        while queue:
            path = queue.pop(0)
            links = await render(path)
            routes.append(path)
            for href in links:
                h = href.split("#")[0].split("?")[0] or "/"
                if h.startswith(SKIP) or h in seen or h.startswith("/immopedia/"):
                    continue
                seen.add(h); queue.append(h)
            print(f"{len(routes):4d} {path}")
        if WITH_IMMOPEDIA:
            for i, path in enumerate(imm_routes):
                await render(path)
                if i % 100 == 0: print(f"     immopedia {i}/{len(imm_routes)}")
        await b.close()
    return routes, imm_routes


def write_sitemap(routes, imm_routes):
    today = datetime.date.today().isoformat()
    urls = [r for r in routes if not r.startswith(NOINDEX)] + imm_routes
    def prio(r):
        return "1.0" if r == "/" else "0.8" if r.count("/") == 1 else "0.6"
    body = "\n".join(f"  <url><loc>{SITE_URL}{r}</loc><lastmod>{today}</lastmod><priority>{prio(r)}</priority></url>" for r in sorted(set(urls)))
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n', encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /mein-bereich\n\n# Kurzprofil für KI-Assistenten: {SITE_URL}/llms.txt\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"sitemap.xml: {len(set(urls))} URLs")


def main():
    if not (DIST / "index.html").exists():
        raise SystemExit("Bitte zuerst `npm run build` ausführen.")
    # Cloudflare Pages: ohne 404.html greift der native SPA-Fallback (Root-index
    # für unbekannte Pfade). Kein /* → app.html in _redirects – das kollidiert
    # mit Pages-Pretty-URLs (/app.html → /app) und leitet die ganze Site um.
    server = subprocess.Popen(["npx", "vite", "preview", "--port", str(PORT), "--strictPort"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_for_server()
        routes, imm_routes = asyncio.run(render_all())
        write_sitemap(routes, imm_routes)
    finally:
        server.terminate()


if __name__ == "__main__":
    main()
