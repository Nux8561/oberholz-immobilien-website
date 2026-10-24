"""Vollständiges HTML, Sitemap, Robots und echte Fehlerseite für Cloudflare Pages.

npm run build:seo rendert alle Inhaltsseiten einschließlich sämtlicher Immopedia-
Einträge. Ein Build bricht bei fehlendem Inhalt oder fehlerhaften Metadaten ab.
"""
import asyncio
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
PORT = 4174
BASE = f'http://localhost:{PORT}'
SITE_URL = re.search(r"SITE_URL = '([^']+)'", (ROOT / 'src/data/routes.ts').read_text()).group(1)
SKIP = ('/downloads/', '/assets/', '/data/')


def wait_for_server():
    for _ in range(60):
        try:
            urllib.request.urlopen(BASE, timeout=1)
            return
        except Exception:
            time.sleep(.5)
    raise RuntimeError('Vite Preview startet nicht')


async def render_all():
    index = json.loads((ROOT / 'public/data/immopedia/index.json').read_text())
    terms = [f"/immopedia/{e['slug']}" for e in index]
    queue = asyncio.Queue()
    seen = set(terms) | {'/'}
    await queue.put('/')
    for path in terms:
        await queue.put(path)
    routes, failures = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(locale='de-DE', viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')

        async def render(page, path):
            await page.goto(BASE + path, wait_until='domcontentloaded')
            await page.wait_for_function("""expectedCanonical => {
              const h = document.querySelector('main h1');
              const ld = document.querySelector('#ld-page');
              return h?.textContent.trim() && ld && document.querySelector('link[rel=canonical]')?.href === expectedCanonical && !document.querySelector('.ipedia__msg')?.textContent.includes('Wird geladen');
            }""", arg=SITE_URL + path.rstrip('/') + '/', timeout=15000)
            if path == '/immopedia':
                await page.wait_for_selector('.ipedia__list a')
            if path.startswith('/immopedia/'):
                await page.wait_for_selector('.ipedia__body .rich__p')
                await page.wait_for_function("document.querySelector('#ld-page').textContent.includes('DefinedTerm')")
            info = await page.evaluate("""() => ({
              title: document.title,
              h1: [...document.querySelectorAll('main h1')].map(e => e.textContent.trim()),
              canonical: document.querySelector('link[rel=canonical]')?.href,
              description: document.querySelector('meta[name=description]')?.content,
              noindex: document.querySelector('meta[name=robots]')?.content.includes('noindex'),
              notFound: !!document.querySelector('main')?.textContent.includes('Diese Seite gibt es nicht'),
              links: [...document.querySelectorAll('a[href^="/"]')].map(e => e.getAttribute('href'))
            })""")
            if info['notFound'] or len(info['h1']) != 1 or not info['description']:
                raise ValueError(f"Unvollständiger Inhalt: {info['h1']}")
            if info['canonical'] != SITE_URL + path.rstrip('/') + '/':
                raise ValueError(f"Falsches Canonical: {info['canonical']}")
            out = DIST / path.strip('/') / 'index.html' if path != '/' else DIST / 'index.html'
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(await page.content(), encoding='utf-8')
            return info

        async def worker():
            page = await ctx.new_page()
            while True:
                path = await queue.get()
                try:
                    info = await render(page, path)
                    if not info['noindex']:
                        routes.append(path)
                    for href in info['links']:
                        h = urlsplit(href).path or '/'
                        if h in seen or h.startswith(SKIP):
                            continue
                        seen.add(h)
                        await queue.put(h)
                    if len(routes) % 100 == 0 or not path.startswith('/immopedia/'):
                        print(f'{len(routes):4d} {path}', flush=True)
                except Exception as exc:
                    failures.append(f'{path}: {exc}')
                finally:
                    queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(6)]
        await queue.join()
        for worker_task in workers:
            worker_task.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
        # Cloudflare liefert unbekannte URLs mit HTTP 404 aus. Die React-Routen
        # bleiben nach dem Laden interaktiv; bekannte Seiten liegen vollständig vor.
        page = await ctx.new_page()
        await page.goto(BASE + '/gibt-es-nicht', wait_until='networkidle')
        await page.wait_for_selector('meta[name=robots][content="noindex, follow"]', state='attached')
        (DIST / '404.html').write_text(await page.content(), encoding='utf-8')
        await browser.close()
    if failures:
        raise RuntimeError('\n'.join(failures))
    return routes


def write_outputs(routes):
    body = '\n'.join(f"  <url><loc>{escape(SITE_URL + path.rstrip('/') + '/')}</loc></url>" for path in sorted(set(routes)))
    (DIST / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '\n</urlset>\n', encoding='utf-8')
    (DIST / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /mein-bereich\n\nSitemap: {SITE_URL}/sitemap.xml\n', encoding='utf-8')
    (DIST / '_redirects').write_text('''/immobilien /immobilien/kaufen 301
/commercial /kapitalanlage 301
/magazin /ratgeber 301
/magazin/* /ratgeber 301
/standorte /regionen 301
/stadt/essen /regionen/essen 301
/stadt/muenster /regionen/muenster 301
/stadt/* /regionen 301
/makler-werden /ueber-uns 301
/kontakt/muenster /regionen/muenster 301
/kontakt/essen /regionen/essen 301
/kontakt/bochum /regionen 301
/leistungen /verkaufen 301
/vermarktung /verkaufen 301
/wohnung-kaufen /immobilien/kaufen?typ=Wohnung 301
/service /ratgeber#rechner 301
/downloads /ratgeber#downloads 301
/ueber-uns/qualifikation /ueber-uns#qualifikation 301
/ueber-uns/iso-9001 /ueber-uns#qualitaet 301
/regionen/bochum /regionen 301
/regionen/bochum/verkaufen /verkaufen 301
/regionen/bochum/immobilienbewertung /bewertung 301
/regionen/bochum/wohnung-verkaufen /verkaufen 301
''', encoding='utf-8')
    print(f'Sitemap: {len(set(routes))} vollständig gerenderte URLs; 404 und 301-Weiterleitungen erstellt.', flush=True)


def main():
    if not (DIST / 'index.html').exists():
        raise SystemExit('Bitte zuerst npm run build ausführen.')
    server = subprocess.Popen(['npx', 'vite', 'preview', '--port', str(PORT), '--strictPort'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_for_server()
        write_outputs(asyncio.run(render_all()))
    finally:
        server.terminate()
        server.wait(timeout=10)


if __name__ == '__main__':
    main()
