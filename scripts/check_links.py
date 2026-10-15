"""Link-Prüfung der lokalen Website (Playwright). Aufruf: python3 scripts/check_links.py  (Dev-Server auf :5173)

Startet bei "/", folgt allen internen Links (Breitensuche) und meldet je Seite:
404-Seiten, Konsolen-/JS-Fehler, fehlgeschlagene Requests (>= 400), Links ohne Ziel (data-missing-route),
leere href="#"-Links sowie horizontales Overflow bei 390 px. Immopedia: alle Index-Slugs müssen als JSON existieren,
im Browser wird eine Stichprobe geöffnet. Bericht: analysis/link-check.json
"""
import asyncio, json, random, sys
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from _common import LOCAL_URL, ROOT

BASE = LOCAL_URL.rstrip("/")
SKIP_PREFIX = ("/downloads/", "/assets/", "/data/")
IMMOPEDIA_SAMPLE = 25
MAX_QUERY_PAGES = 40  # Such-URLs mit Filtern (?ort=…): Stichprobe


def norm(href: str):
    u = urlparse(href)
    if u.scheme not in ("http", "https") or u.netloc != urlparse(BASE).netloc:
        return None
    path = u.path or "/"
    if path.startswith(SKIP_PREFIX):
        return None
    return path + (f"?{u.query}" if u.query else "")


async def check_page(page, path, width):
    errors, bad = [], []
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("response", lambda r: r.status >= 400 and bad.append(f"{r.status} {r.url}"))
    await page.set_viewport_size({"width": width, "height": 900})
    await page.goto(BASE + path, wait_until="load")
    await page.wait_for_load_state("networkidle", timeout=8000)
    await page.wait_for_timeout(100)
    info = await page.evaluate("""() => ({
      notFound: !!document.querySelector('main') && document.querySelector('main').innerText.includes('Diese Seite gibt es nicht'),
      missing: [...document.querySelectorAll('[data-missing-route]')].map(a => a.textContent.trim()),
      deadHash: [...document.querySelectorAll('a[href="#"]')].map(a => a.textContent.trim()),
      overflow: document.documentElement.scrollWidth - window.innerWidth,
      title: document.title,
      links: [...document.querySelectorAll('a[href]')].map(a => a.href),
      downloads: [...document.querySelectorAll('a[href^="/downloads/"], a[href*="/downloads/"]')].map(a => a.getAttribute('href')),
    })""")
    return info, errors, bad


async def main():
    report, problems = {}, []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(locale="de-DE")
        queue, seen = ["/"], {"/"}
        downloads = set()
        while queue:
            path = queue.pop(0)
            page = await ctx.new_page()
            try:
                info, errors, bad = await check_page(page, path, 1440)
            except Exception as e:  # noqa: BLE001
                problems.append(f"{path}: Ladefehler {e}")
                await page.close(); continue
            await page.close()
            downloads.update(d for d in info["downloads"] if d)
            entry = {"title": info["title"], "errors": errors, "bad": bad, "missing": info["missing"], "deadHash": info["deadHash"], "notFound": info["notFound"]}
            report[path] = entry
            if info["notFound"]: problems.append(f"{path}: 404-Seite")
            if errors: problems.append(f"{path}: Konsole {errors[:2]}")
            if bad: problems.append(f"{path}: Requests {bad[:3]}")
            if info["missing"]: problems.append(f"{path}: Links ohne Ziel {info['missing'][:5]}")
            if info["deadHash"]: problems.append(f"{path}: href='#' {info['deadHash'][:5]}")
            for href in info["links"]:
                n = norm(href)
                if not n or n in seen:
                    continue
                # Immopedia-Begriffe nur als Stichprobe, Suchvarianten (?ort=…) einmal je Ziel
                if n.startswith("/immopedia/"):
                    continue
                if "?" in n and sum(1 for q in seen if "?" in q) >= MAX_QUERY_PAGES:
                    continue
                seen.add(n); queue.append(n)
            print(f"{len(report):4d} ok  {path}" if not (info["notFound"] or errors or bad or info["missing"] or info["deadHash"]) else f"{len(report):4d} !!  {path}")

        # Immopedia: Dateien vollständig, Stichprobe im Browser
        idx = json.loads((ROOT / "public/data/immopedia/index.json").read_text())
        missing_files = [e["slug"] for e in idx if not (ROOT / "public/data/immopedia" / f"{e['slug']}.json").exists()]
        if missing_files: problems.append(f"Immopedia: {len(missing_files)} fehlende JSON-Dateien, z. B. {missing_files[:5]}")
        random.seed(7)
        for e in random.sample(idx, IMMOPEDIA_SAMPLE):
            page = await ctx.new_page()
            info, errors, bad = await check_page(page, f"/immopedia/{e['slug']}", 1440)
            await page.close()
            if info["notFound"] or errors or bad: problems.append(f"/immopedia/{e['slug']}: {errors[:1]} {bad[:1]}")
        report["_immopedia"] = {"terms": len(idx), "missingFiles": len(missing_files), "sample": IMMOPEDIA_SAMPLE}

        # PDFs
        for d in sorted(downloads):
            if not (ROOT / "public" / d.lstrip("/")).exists(): problems.append(f"Download fehlt: {d}")
        report["_downloads"] = sorted(downloads)

        # Mobile Overflow (390 px) für alle Seiten ohne Query
        mob = await b.new_context(locale="de-DE", viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        for path in [k for k in report if not k.startswith("_") and "?" not in k]:
            page = await mob.new_page()
            await page.goto(BASE + path, wait_until="networkidle")
            ov = await page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            if ov > 0:
                culprit = await page.evaluate("""() => { const w = innerWidth; return [...document.querySelectorAll('body *')]
                  .filter(e => e.getBoundingClientRect().right > w + 1).slice(-3).map(e => e.tagName + '.' + [...e.classList].join('.')) }""")
                problems.append(f"{path}: Overflow {ov}px bei 390 ({culprit})")
            await page.close()
        await b.close()

    out = ROOT / "analysis" / "link-check.json"
    out.write_text(json.dumps({"pages": len([k for k in report if not k.startswith('_')]), "problems": problems, "report": report}, ensure_ascii=False, indent=1))
    print(f"\n{len([k for k in report if not k.startswith('_')])} Seiten geprüft, {len(problems)} Probleme")
    for x in problems: print(" -", x)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    asyncio.run(main())
