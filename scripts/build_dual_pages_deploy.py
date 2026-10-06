"""Build dual Cloudflare Pages deploys: main + regionen, cross-linked."""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_ORIGIN = "https://oberholz-immobilien.pages.dev"
REGIONEN_ORIGIN = "https://oberholz-regionen.pages.dev"

DIST_MAIN = ROOT / "dist"
DIST_REGIONEN = ROOT / "dist-regionen"
PUBLIC = ROOT / "public"

# Absolute site paths that stay on the regionen host
REGIONEN_PATH_RE = re.compile(r"^/regionen(?:/|$|\?)")

# CSS/Fonts/Icons must be same-origin on regionen (not cross-origin from main).
# /media stays on main (~1.5GB). These folders are small enough to ship twice.
LOCAL_STATIC_PREFIXES = (
    "/theme/",
    "/assets/",
    "/mediatypes/",
    "/images/",
)
LOCAL_STATIC_FILES = (
    "/favicon.ico",
    "/robots.txt",
    "/site.webmanifest",
)

# Folders copied from dist/ into dist-regionen for same-origin assets
REGIONEN_STATIC_FOLDERS = ("theme", "assets", "mediatypes", "images")

ATTR_RE = re.compile(
    r"""\b(href|src|action|poster|data-src|content)=(["'])(/(?!/)[^"']*)\2""",
    re.IGNORECASE,
)
SRCSET_RE = re.compile(
    r"""\b(?:srcset|imagesrcset)=(["'])([^"']+)\1""",
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(r"""url\((['"]?)(/(?!/)[^'")]+)\1\)""", re.IGNORECASE)

MAIN_ABS_LOCAL_RE = re.compile(
    r"""https://oberholz-immobilien\.pages\.dev(/(?:theme|assets|mediatypes|images)/[^"'\\\s]*)""",
    re.IGNORECASE,
)


def is_local_static(path: str) -> bool:
    if path in LOCAL_STATIC_FILES:
        return True
    return any(path.startswith(prefix) for prefix in LOCAL_STATIC_PREFIXES)


def rewrite_path(path: str, *, keep_regionen_local: bool) -> str:
    if path.startswith("//") or path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        return path
    if keep_regionen_local and REGIONEN_PATH_RE.match(path):
        return path
    if keep_regionen_local and is_local_static(path):
        return path
    # overview page lives on main
    if path == "/regionen.html" or path.startswith("/regionen.html?"):
        return MAIN_ORIGIN + path
    if keep_regionen_local:
        return MAIN_ORIGIN + path
    # main site: send /regionen/* to regionen project
    if REGIONEN_PATH_RE.match(path):
        return REGIONEN_ORIGIN + path
    return path


def rewrite_html(html: str, *, keep_regionen_local: bool) -> str:
    def attr_sub(m: re.Match[str]) -> str:
        attr, q, path = m.group(1), m.group(2), m.group(3)
        new = rewrite_path(path, keep_regionen_local=keep_regionen_local)
        return f"{attr}={q}{new}{q}"

    html = ATTR_RE.sub(attr_sub, html)

    def srcset_sub(m: re.Match[str]) -> str:
        q, value = m.group(1), m.group(2)
        parts = []
        for chunk in value.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            bits = chunk.split()
            bits[0] = rewrite_path(bits[0], keep_regionen_local=keep_regionen_local)
            parts.append(" ".join(bits))
        return f"srcset={q}{', '.join(parts)}{q}"

    html = SRCSET_RE.sub(srcset_sub, html)

    def css_sub(m: re.Match[str]) -> str:
        q, path = m.group(1), m.group(2)
        new = rewrite_path(path, keep_regionen_local=keep_regionen_local)
        return f"url({q}{new}{q})"

    html = CSS_URL_RE.sub(css_sub, html)
    return html


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_regionen_static() -> None:
    """Ship CSS/fonts/icons on the regionen project (same-origin)."""
    if not DIST_MAIN.exists():
        raise SystemExit("dist/ missing – run npm run build first")
    DIST_REGIONEN.mkdir(parents=True, exist_ok=True)
    for name in REGIONEN_STATIC_FOLDERS:
        src = DIST_MAIN / name
        if not src.exists():
            print(f"skip missing static folder: {name}", flush=True)
            continue
        dst = DIST_REGIONEN / name
        print(f"copying dist/{name} -> dist-regionen/{name} ...", flush=True)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    for name in ("favicon.ico", "robots.txt", "site.webmanifest"):
        src = DIST_MAIN / name
        if src.is_file():
            shutil.copy2(src, DIST_REGIONEN / name)


def localize_regionen_asset_urls() -> int:
    """Turn Main absolute theme/assets URLs back into same-origin paths."""
    from concurrent.futures import ProcessPoolExecutor, as_completed

    target = DIST_REGIONEN / "regionen"
    if not target.exists():
        raise SystemExit(f"missing {target}")
    paths = list(target.rglob("*.html")) + list(DIST_REGIONEN.glob("*.html"))
    print(f"localize asset urls candidates={len(paths)}", flush=True)
    changed = 0
    done = 0
    workers = min(8, max(2, (os.cpu_count() or 4)))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_localize_one_html, path): path for path in paths}
        for fut in as_completed(futures):
            done += 1
            if done % 2000 == 0:
                print(f"localize asset urls {done}/{len(paths)}...", flush=True)
            try:
                if fut.result():
                    changed += 1
            except Exception as exc:  # noqa: BLE001
                print(f"localize failed {futures[fut]}: {exc}", flush=True)
    print(f"localized asset urls files={done} changed={changed}", flush=True)
    return changed


def _localize_one_html(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    new = MAIN_ABS_LOCAL_RE.sub(r"\1", raw)
    if new == raw:
        return False
    path.write_text(new, encoding="utf-8", newline="")
    return True


def build_regionen() -> int:
    if DIST_REGIONEN.exists():
        shutil.rmtree(DIST_REGIONEN)
    DIST_REGIONEN.mkdir(parents=True)
    target = DIST_REGIONEN / "regionen"
    print("copying public/regionen -> dist-regionen/regionen ...", flush=True)
    shutil.copytree(PUBLIC / "regionen", target)
    copy_regionen_static()

    # optional alphabet landing if present at public root
    overview = PUBLIC / "regionen.html"
    if overview.exists():
        # keep overview on main; still useful mirror with links rewritten to main for non-regionen
        html = overview.read_text(encoding="utf-8", errors="replace")
        (DIST_REGIONEN / "regionen.html").write_text(
            rewrite_html(html, keep_regionen_local=True),
            encoding="utf-8",
            newline="",
        )

    count = 0
    changed = 0
    for path in target.rglob("*.html"):
        count += 1
        if count % 2000 == 0:
            print(f"rewrite regionen html {count}...", flush=True)
        raw = path.read_text(encoding="utf-8", errors="replace")
        new = rewrite_html(raw, keep_regionen_local=True)
        if new != raw:
            path.write_text(new, encoding="utf-8", newline="")
            changed += 1
    print(f"regionen html files={count} rewritten={changed}", flush=True)
    return count


def patch_main_dist() -> None:
    if not DIST_MAIN.exists():
        raise SystemExit("dist/ missing – run npm run build first")

    # After SEO cleanup only Bochum/Essen/Münster remain (~8 HTML files).
    # Keep /regionen on the main Pages project (no sibling redirect needed).
    regionen_dir = DIST_MAIN / "regionen"
    if not regionen_dir.exists() and (PUBLIC / "regionen").exists():
        print("copying public/regionen into dist/regionen ...", flush=True)
        shutil.copytree(PUBLIC / "regionen", regionen_dir)

    redirects = DIST_MAIN / "_redirects"
    # Prefer public/_redirects from Vite build; ensure Münster canonical rules exist.
    public_redirects = PUBLIC / "_redirects"
    if public_redirects.is_file():
        redirects.write_text(
            public_redirects.read_text(encoding="utf-8"),
            encoding="utf-8",
            newline="\n",
        )
    else:
        redirects.write_text(
            "\n".join(
                [
                    "# Canonical Münster",
                    "/regionen/munster  /regionen/muenster/immobilienmakler.html  301",
                    "/regionen/munster/  /regionen/muenster/immobilienmakler.html  301",
                    "/regionen/munster/*  /regionen/muenster/:splat  301",
                    "",
                ]
            ),
            encoding="utf-8",
            newline="\n",
        )
    print("wrote dist/_redirects", flush=True)

    # Ensure /regionen links stay same-origin (undo any absolute regionen-host rewrites)
    html_files = list(DIST_MAIN.rglob("*.html"))
    changed = 0
    abs_regionen = re.compile(
        re.escape(REGIONEN_ORIGIN) + r"(/regionen(?:/[^\"'\\s]*)?)",
        re.I,
    )
    for i, path in enumerate(html_files, 1):
        if i % 2000 == 0:
            print(f"patch main html {i}/{len(html_files)}...", flush=True)
        raw = path.read_text(encoding="utf-8", errors="replace")
        new = abs_regionen.sub(r"\1", raw)
        if new != raw:
            path.write_text(new, encoding="utf-8", newline="")
            changed += 1
    print(f"main html regionen-host normalized={changed}/{len(html_files)}", flush=True)


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "localize-static":
        # Fast path: keep existing regionen HTML, only fix asset origins + copy static
        copy_regionen_static()
        localize_regionen_asset_urls()
        files = sum(1 for _ in DIST_REGIONEN.rglob("*") if _.is_file())
        print(f"dist-regionen total files={files}", flush=True)
    elif mode == "rewrite-regionen":
        target = DIST_REGIONEN / "regionen"
        if not target.exists():
            raise SystemExit(f"missing {target}")
        copy_regionen_static()
        overview = PUBLIC / "regionen.html"
        if overview.exists():
            html = overview.read_text(encoding="utf-8", errors="replace")
            (DIST_REGIONEN / "regionen.html").write_text(
                rewrite_html(html, keep_regionen_local=True),
                encoding="utf-8",
                newline="",
            )
        count = 0
        changed = 0
        for path in target.rglob("*.html"):
            count += 1
            if count % 2000 == 0:
                print(f"rewrite regionen html {count}...", flush=True)
            raw = path.read_text(encoding="utf-8", errors="replace")
            # First strip any previous Main absolute local-static URLs, then rewrite
            raw = MAIN_ABS_LOCAL_RE.sub(r"\1", raw)
            new = rewrite_html(raw, keep_regionen_local=True)
            if new != raw:
                path.write_text(new, encoding="utf-8", newline="")
                changed += 1
        print(f"regionen html files={count} rewritten={changed}", flush=True)
        files = sum(1 for _ in DIST_REGIONEN.rglob("*") if _.is_file())
        print(f"dist-regionen total files={files}", flush=True)
    elif mode in ("all", "regionen"):
        build_regionen()
        files = sum(1 for _ in DIST_REGIONEN.rglob("*") if _.is_file())
        print(f"dist-regionen total files={files}", flush=True)
    if mode in ("all", "main"):
        patch_main_dist()
        files = sum(1 for _ in DIST_MAIN.rglob("*") if _.is_file())
        print(f"dist main total files={files}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
