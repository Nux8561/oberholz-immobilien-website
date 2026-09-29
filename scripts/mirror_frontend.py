"""Mirror the public homepage frontend for local reconstruction.

Downloads only same-origin public assets. Strips analytics. Blocks lead submission.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ANALYSIS = ROOT / "analysis"
ORIGIN = "https://www.immobilien-experten.de"
URL = ORIGIN + "/"

SKIP_PARTS = (
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
    "facebook.com",
    "facebook.net",
    "hotjar.com",
    "clarity.ms",
    "index.php",
)

SESSION = requests.Session()
SESSION.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def same_origin_path(raw: str, base: str) -> str | None:
    raw = raw.strip().strip("\"' ")
    if not raw or raw.startswith("data:") or raw.startswith("#") or raw.startswith("mailto:") or raw.startswith("tel:"):
        return None
    if raw.startswith("javascript:"):
        return None
    absolute = urljoin(base, raw)
    parsed = urlparse(absolute)
    if parsed.scheme not in ("http", "https"):
        return None
    host = parsed.netloc.lower()
    if host not in ("www.immobilien-experten.de", "immobilien-experten.de"):
        return None
    if any(part in absolute for part in SKIP_PARTS):
        return None
    path = unquote(parsed.path)
    if not path or path.endswith("/"):
        return None
    return path


def local_file(path: str) -> Path:
    rel = path.lstrip("/").replace("\\", "/")
    return PUBLIC / rel


def extract_css_urls(css: str, base: str) -> list[str]:
    found = []
    for match in re.finditer(r"url\(\s*([^)]+?)\s*\)", css):
        path = same_origin_path(match.group(1), base)
        if path:
            found.append(path)
    for match in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\"\)]+)", css):
        path = same_origin_path(match.group(1), base)
        if path:
            found.append(path)
    return found


def collect_from_html(html: str) -> set[str]:
    paths: set[str] = set()
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(True):
        for attr in ("src", "href", "poster"):
            val = tag.get(attr)
            if isinstance(val, str):
                path = same_origin_path(val, URL)
                if path and not path.endswith(".html"):
                    paths.add(path)
        srcset = tag.get("srcset")
        if isinstance(srcset, str):
            for part in srcset.split(","):
                bit = part.strip().split(" ")[0]
                path = same_origin_path(bit, URL)
                if path:
                    paths.add(path)
        style = tag.get("style")
        if isinstance(style, str):
            paths.update(extract_css_urls(style, URL))
    for style in soup.find_all("style"):
        paths.update(extract_css_urls(style.get_text() or "", URL))
    return paths


def download(path: str, mapping: list[dict]) -> str | None:
    dest = local_file(path)
    url = ORIGIN + path
    if dest.exists() and dest.stat().st_size > 0:
        mapping.append({"original_url": url, "local_path": "/" + path.lstrip("/"), "status": "cached"})
        return dest.read_text(encoding="utf-8", errors="ignore") if dest.suffix.lower() == ".css" else None
    try:
        response = SESSION.get(url, timeout=60)
    except requests.RequestException as exc:
        mapping.append({"original_url": url, "local_path": "/" + path.lstrip("/"), "status": f"error:{exc}"})
        return None
    if response.status_code != 200 or not response.content:
        mapping.append({"original_url": url, "local_path": "/" + path.lstrip("/"), "status": f"http:{response.status_code}"})
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)
    mapping.append({"original_url": url, "local_path": "/" + path.lstrip("/"), "status": "ok", "bytes": len(response.content)})
    if dest.suffix.lower() == ".css":
        return response.text
    return None


def patch_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for script in list(soup.find_all("script")):
        src = script.get("src") or ""
        text = script.string or script.get_text() or ""
        if any(part in src for part in ("googletagmanager", "google-analytics", "gtag/js")):
            script.decompose()
            continue
        if "function gtag(" in text or "gtag('config'" in text or "gtag(\"config\"" in text:
            script.decompose()
            continue

    for iframe in list(soup.find_all("iframe")):
        src = iframe.get("src") or ""
        if "googletagmanager" in src or "doubleclick" in src:
            parent = iframe.parent
            iframe.decompose()
            if parent and parent.name == "noscript" and not parent.get_text(strip=True) and not parent.find():
                parent.decompose()

    form = soup.select_one("#iwf-form")
    if form:
        form["action"] = "#iwf"
        form["method"] = "get"
        form["onsubmit"] = "event.preventDefault();"

    html_out = str(soup)
    html_out = html_out.replace("var doPoll = true;", "var doPoll = false;")
    old = "if (!ok) { e.preventDefault(); }"
    new = """e.preventDefault();
if (!ok) { return; }
form.querySelectorAll('.iwf-step').forEach(function (s) { s.classList.remove('is-active'); });
var done = document.getElementById('iwf-local-success');
if (!done) {
  done = document.createElement('section');
  done.id = 'iwf-local-success';
  done.className = 'iwf-step is-active';
  done.innerHTML = '<span class="iwf-kicker">Immobilien-Vermittlung</span><h3 class="iwf-q">Demo submission successful</h3><p class="iwf-sub">Die Anfrage bleibt auf diesem Geraet und wurde nicht versendet.</p>';
  form.appendChild(done);
} else {
  done.classList.add('is-active');
}
if (globalNav) { globalNav.style.display = 'none'; }
if (bar) { bar.style.width = '100%'; }
return;"""
    if old not in html_out:
        raise SystemExit("form submit patch point missing")
    html_out = html_out.replace(old, new, 1)

    old_fetch = "fetch('/index.php?rex-api-call=contact_widget', { method: 'POST', body: formData })"
    new_fetch = "Promise.resolve({ text: function () { return Promise.resolve('<div class=\"cw-local-panel\" style=\"position:fixed;right:24px;bottom:130px;z-index:2000;background:#fff;padding:16px 18px;width:280px;border-radius:12px;box-shadow:0 10px 28px rgba(34,58,102,.18);color:#223a66;font-family:Roboto,sans-serif\"><strong>Kontakt</strong><p style=\"margin:8px 0 0;color:#5b595a;font-size:14px\">Lokale Ansicht. Es wird keine Anfrage gesendet.</p></div>'); } })"
    if old_fetch not in html_out:
        raise SystemExit("widget fetch patch point missing")
    html_out = html_out.replace(old_fetch, new_fetch, 1)

    guard = """<script>
window.fetch = function (input, init) {
  var url = typeof input === 'string' ? input : (input && input.url) || '';
  if (/rex-api-call|immobilien-experten\\.de|googletagmanager|google-analytics|facebook|doubleclick|hotjar/.test(url)) {
    return Promise.resolve(new Response('', { status: 204 }));
  }
  return fetch.__native(input, init);
};
window.fetch.__native = window.fetch;
</script>"""
    # The assignment above shadows fetch before saving native. Fix properly.
    guard = """<script>
(function () {
  var nativeFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    if (/rex-api-call|immobilien-experten\\.de|googletagmanager|google-analytics|facebook|doubleclick|hotjar/.test(url)) {
      return Promise.resolve(new Response('', { status: 204 }));
    }
    return nativeFetch(input, init);
  };
  var NativeXHR = window.XMLHttpRequest;
  window.XMLHttpRequest = function () {
    var xhr = new NativeXHR();
    var open = xhr.open;
    xhr.open = function (method, url) {
      if (/rex-api-call|immobilien-experten\\.de|googletagmanager|google-analytics|facebook|doubleclick/.test(String(url))) {
        url = 'about:blank';
      }
      return open.apply(xhr, [method, url].concat([].slice.call(arguments, 2)));
    };
    return xhr;
  };
})();
</script>"""
    html_out = html_out.replace("<head>", "<head>" + guard, 1)
    return html_out


def capture() -> tuple[str, list[dict]]:
    network = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, locale="de-DE")

        def on_response(response):
            request = response.request
            network.append(
                {
                    "url": response.url,
                    "status": response.status,
                    "resource_type": request.resource_type,
                    "method": request.method,
                }
            )

        page.on("response", on_response)
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(1200)
        page.evaluate(
            """async () => {
              const height = document.body.scrollHeight;
              for (let y = 0; y < height; y += 700) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 120));
              }
              window.scrollTo(0, 0);
              if (document.fonts && document.fonts.ready) await document.fonts.ready;
            }"""
        )
        page.wait_for_timeout(800)
        html = page.content()
        browser.close()
    return html, network


def main() -> None:
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    html, network = capture()
    (ANALYSIS / "rendered.html").write_text(html, encoding="utf-8")
    (ANALYSIS / "network.json").write_text(json.dumps(network, ensure_ascii=False, indent=2), encoding="utf-8")

    queue = collect_from_html(html)
    for item in network:
        path = same_origin_path(item["url"], URL)
        if not path or path.endswith(".html"):
            continue
        if item["resource_type"] in ("image", "font", "stylesheet", "media", "script", "other"):
            queue.add(path)

    mapping: list[dict] = []
    seen: set[str] = set()
    css_follow: list[str] = []
    pending = sorted(queue)
    while pending:
        path = pending.pop(0)
        if path in seen:
            continue
        seen.add(path)
        if path.endswith(".html"):
            continue
        css_text = download(path, mapping)
        if css_text:
            base = ORIGIN + path
            for extra in extract_css_urls(css_text, base):
                if extra not in seen:
                    pending.append(extra)

    cleaned = patch_html(html)
    (ROOT / "index.html").write_text(cleaned, encoding="utf-8")
    (ANALYSIS / "assets.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for item in mapping if item["status"] in ("ok", "cached"))
    bad = [item for item in mapping if item["status"] not in ("ok", "cached")]
    print(f"assets ok={ok} failed={len(bad)} index={len(cleaned)}")
    for item in bad[:30]:
        print("FAIL", item["status"], item["original_url"])


if __name__ == "__main__":
    main()
