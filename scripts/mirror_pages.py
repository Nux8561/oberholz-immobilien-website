"""Mirror every public HTML page from the sitemap into public/.

Shared base CSS is stored once. Tracking is removed. Lead posts are blocked.
"""
from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ANALYSIS = ROOT / "analysis"
ORIGIN = "https://www.immobilien-experten.de"
SITEMAP = ANALYSIS / "sitemap_urls.txt"
SHARED_CSS = PUBLIC / "theme" / "shared-base.css"
WORKERS = 10

SKIP_HOST_PARTS = (
    "googletagmanager.com",
    "google-analytics.com",
    "googleadservices.com",
    "doubleclick.net",
    "facebook.com",
    "facebook.net",
    "hotjar.com",
    "clarity.ms",
)

GUARD = """<script id="local-request-guard">
(function () {
  var nativeFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    if (/rex-api-call|immobilien-experten\\.de|googletagmanager|google-analytics|facebook|doubleclick|hotjar/.test(url)) {
      return Promise.resolve(new Response('', { status: 204 }));
    }
    return nativeFetch(input, init);
  };
  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form || form.tagName !== 'FORM') return;
    var method = (form.getAttribute('method') || 'get').toLowerCase();
    var action = form.getAttribute('action') || '';
    if (method === 'post' || /rex-api|index\\.php|iwf/.test(action)) {
      event.preventDefault();
      event.stopPropagation();
      if (!document.getElementById('local-form-notice')) {
        var note = document.createElement('div');
        note.id = 'local-form-notice';
        note.setAttribute('role', 'status');
        note.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:3000;background:#223a66;color:#fff;padding:14px 18px;border-radius:10px;font-family:Roboto,sans-serif;max-width:420px;text-align:center';
        note.textContent = 'Demo submission successful. Die Anfrage wurde nur lokal angezeigt und nicht versendet.';
        document.body.appendChild(note);
      }
    }
  }, true);
})();
</script>"""

STYLE_START = '<style media="">@font-face { font-family: "Lato"'
THREAD = threading.local()
LOCK = threading.Lock()
ASSETS: set[str] = set()
STATS = {"ok": 0, "skip": 0, "fail": 0, "css_shared": 0, "css_kept": 0}
FAILURES: list[dict] = []


def session() -> requests.Session:
    current = getattr(THREAD, "session", None)
    if current is None:
        current = requests.Session()
        current.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        THREAD.session = current
    return current


def same_origin_path(raw: str, base: str) -> str | None:
    raw = raw.strip().strip("\"'")
    if not raw or raw.startswith(("data:", "#", "mailto:", "tel:", "javascript:")):
        return None
    absolute = urljoin(base, raw)
    parsed = urlparse(absolute)
    if parsed.scheme not in ("http", "https"):
        return None
    if parsed.netloc.lower() not in ("www.immobilien-experten.de", "immobilien-experten.de", ""):
        return None
    if any(part in absolute for part in SKIP_HOST_PARTS):
        return None
    if "index.php" in parsed.path:
        return None
    path = unquote(parsed.path)
    if not path or path.endswith("/"):
        return None
    return path


def collect_assets(html: str, page_url: str) -> set[str]:
    found: set[str] = set()
    for match in re.finditer(r"""(?:src|href|poster|data-src)=["']([^"']+)["']""", html):
        path = same_origin_path(match.group(1), page_url)
        if path and not path.endswith(".html"):
            found.add(path)
    for match in re.finditer(r"""srcset=["']([^"']+)["']""", html):
        for part in match.group(1).split(","):
            bit = part.strip().split(" ")[0]
            path = same_origin_path(bit, page_url)
            if path and not path.endswith(".html"):
                found.add(path)
    for match in re.finditer(r"url\(\s*([^)]+?)\s*\)", html):
        path = same_origin_path(match.group(1), page_url)
        if path and not path.endswith(".html"):
            found.add(path)
    return found


def clean_html(html: str, shared_hash: str) -> str:
    html = re.sub(
        r"<script[^>]+src=[\"']https://www\.googletagmanager\.com[^\"']+[\"'][^>]*>\s*</script>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<script>window\.dataLayer = window\.dataLayer \|\| \[\];function gtag\(\)\{.*?</script>",
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"<noscript>\s*<iframe[^>]+googletagmanager\.com.*?</iframe>\s*</noscript>",
        "",
        html,
        count=1,
        flags=re.I | re.S,
    )
    html = html.replace("var doPoll = true;", "var doPoll = false;")
    old_fetch = "fetch('/index.php?rex-api-call=contact_widget', { method: 'POST', body: formData })"
    new_fetch = (
        "Promise.resolve({ text: function () { return Promise.resolve("
        "'<div style=\"position:fixed;right:24px;bottom:130px;z-index:2000;background:#fff;"
        "padding:16px 18px;width:280px;border-radius:12px;box-shadow:0 10px 28px rgba(34,58,102,.18);"
        "color:#223a66;font-family:Roboto,sans-serif\"><strong>Kontakt</strong>"
        "<p style=\"margin:8px 0 0;color:#5b595a;font-size:14px\">Lokale Ansicht. Es wird keine Anfrage gesendet.</p></div>'); } })"
    )
    html = html.replace(old_fetch, new_fetch)
    if "local-request-guard" not in html:
        html = re.sub(r"<head[^>]*>", lambda match: match.group(0) + GUARD, html, count=1)

    start = html.find(STYLE_START)
    if start != -1:
        end = html.find("</style>", start)
        inner_start = html.find(">", start) + 1
        inner = html[inner_start:end]
        digest = hashlib.md5(inner.encode("utf-8")).hexdigest()
        if digest == shared_hash:
            html = html[:start] + '<link rel="stylesheet" href="/theme/shared-base.css">' + html[end + len("</style>") :]
            with LOCK:
                STATS["css_shared"] += 1
        else:
            with LOCK:
                STATS["css_kept"] += 1
    return html


def dest_for(path: str) -> Path:
    return PUBLIC / path.lstrip("/")


def fetch(url: str) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = session().get(url, timeout=45)
            if response.status_code in (429, 503):
                time.sleep(1.5 * (attempt + 1))
                continue
            return response
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(0.8 * (attempt + 1))
    if last_error:
        raise last_error
    raise RuntimeError(url)


def mirror_page(path: str, shared_hash: str) -> None:
    if path in ("/", ""):
        with LOCK:
            STATS["skip"] += 1
        return
    dest = dest_for(path)
    if dest.exists() and dest.stat().st_size > 800:
        text = dest.read_text(encoding="utf-8", errors="ignore")
        with LOCK:
            ASSETS.update(collect_assets(text, ORIGIN + path))
            STATS["skip"] += 1
        return
    url = ORIGIN + path
    response = fetch(url)
    content_type = response.headers.get("content-type", "")
    if response.status_code != 200 or ("html" not in content_type and not path.endswith(".html")):
        with LOCK:
            STATS["fail"] += 1
            FAILURES.append({"path": path, "status": response.status_code})
        return
    html = response.content.decode("utf-8", errors="replace")
    with LOCK:
        ASSETS.update(collect_assets(html, url))
    cleaned = clean_html(html, shared_hash)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(cleaned, encoding="utf-8")
    with LOCK:
        STATS["ok"] += 1
        done = STATS["ok"] + STATS["skip"] + STATS["fail"]
        if done % 200 == 0:
            print(f"pages {done} ok={STATS['ok']} skip={STATS['skip']} fail={STATS['fail']}", flush=True)


def download_asset(path: str) -> dict:
    clean_path = path.split("?")[0]
    dest = dest_for(clean_path)
    url = ORIGIN + path
    if dest.exists() and dest.stat().st_size > 0:
        return {"original_url": url, "local_path": clean_path, "status": "cached"}
    try:
        response = fetch(url)
    except requests.RequestException as exc:
        return {"original_url": url, "local_path": clean_path, "status": f"error:{exc}"}
    if response.status_code != 200 or not response.content:
        return {"original_url": url, "local_path": clean_path, "status": f"http:{response.status_code}"}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)
    css_urls: list[str] = []
    if dest.suffix.lower() == ".css":
        css_urls = re.findall(r"url\(\s*([^)]+?)\s*\)", response.text)
    return {
        "original_url": url,
        "local_path": "/" + clean_path.lstrip("/"),
        "status": "ok",
        "bytes": len(response.content),
        "css_urls": css_urls,
        "css_base": ORIGIN + clean_path,
    }


def prepare_shared_css() -> str:
    response = fetch(ORIGIN + "/impressum.html")
    html = response.content.decode("utf-8", errors="replace")
    start = html.find(STYLE_START)
    if start < 0:
        raise SystemExit("shared css block missing")
    end = html.find("</style>", start)
    inner_start = html.find(">", start) + 1
    inner = html[inner_start:end]
    SHARED_CSS.parent.mkdir(parents=True, exist_ok=True)
    SHARED_CSS.write_text(inner, encoding="utf-8")
    digest = hashlib.md5(inner.encode("utf-8")).hexdigest()
    print("shared css", len(inner), digest, flush=True)
    return digest


def main() -> None:
    ANALYSIS.mkdir(parents=True, exist_ok=True)
    paths = []
    for line in SITEMAP.read_text(encoding="utf-8").splitlines():
        parsed = urlparse(line.strip())
        if parsed.netloc and "immobilien-experten.de" not in parsed.netloc:
            continue
        path = unquote(parsed.path)
        if path == "/":
            continue
        if path.endswith(".html"):
            paths.append(path)
    paths = sorted(set(paths))
    print("queue", len(paths), flush=True)
    shared_hash = prepare_shared_css()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(mirror_page, path, shared_hash) for path in paths]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                with LOCK:
                    STATS["fail"] += 1
                    FAILURES.append({"error": str(exc)})

    print("pages done", STATS, "assets", len(ASSETS), flush=True)
    mapping = []
    pending = sorted(ASSETS)
    seen: set[str] = set()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        while pending:
            batch = []
            while pending and len(batch) < 400:
                item = pending.pop(0)
                if item in seen or item.endswith(".html"):
                    continue
                seen.add(item)
                batch.append(item)
            if not batch:
                break
            for result in pool.map(download_asset, batch):
                css_urls = result.pop("css_urls", [])
                css_base = result.pop("css_base", ORIGIN + "/")
                mapping.append(result)
                for raw in css_urls:
                    extra = same_origin_path(raw, css_base)
                    if extra and extra not in seen:
                        pending.append(extra)
            print("assets", len(mapping), "pending", len(pending), flush=True)

    (ANALYSIS / "pages.json").write_text(
        json.dumps(
            {"stats": STATS, "failures": FAILURES[:200], "failure_count": len(FAILURES)},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (ANALYSIS / "page_assets.json").write_text(json.dumps(mapping, ensure_ascii=False), encoding="utf-8")
    print("finished", STATS, "asset records", len(mapping), flush=True)


if __name__ == "__main__":
    main()
