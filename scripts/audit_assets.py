# -*- coding: utf-8 -*-
"""Asset size audit for Oberholz site (read-only analysis)."""
from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC = ROOT / "public"
OUT = ROOT / "analysis" / "asset-audit.md"

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".ico", ".bmp", ".tif", ".tiff"}
VIDEO_EXT = {".mp4", ".webm", ".mov", ".m4v", ".avi", ".mkv"}
FONT_EXT = {".woff", ".woff2", ".ttf", ".otf", ".eot"}
DOC_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx"}


def iter_files(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*"):
        if p.is_file():
            yield p


def main() -> None:
    base = DIST if DIST.exists() else PUBLIC
    files = []
    for p in iter_files(base):
        try:
            size = p.stat().st_size
        except OSError:
            continue
        files.append((p, size))

    total = sum(s for _, s in files)
    by_cat = defaultdict(int)
    by_ext = defaultdict(int)
    for p, s in files:
        ext = p.suffix.lower() or "(none)"
        by_ext[ext] += s
        if ext in IMAGE_EXT:
            by_cat["images"] += s
        elif ext in VIDEO_EXT:
            by_cat["videos"] += s
        elif ext in FONT_EXT:
            by_cat["fonts"] += s
        elif ext in DOC_EXT:
            by_cat["docs"] += s
        elif ext in {".html", ".htm"}:
            by_cat["html"] += s
        elif ext in {".css", ".js", ".mjs", ".map"}:
            by_cat["css_js"] += s
        else:
            by_cat["other"] += s

    largest = sorted(files, key=lambda x: x[1], reverse=True)[:50]

    # Hash duplicates (only files >= 50KB to limit work)
    hashes: dict[str, list[Path]] = defaultdict(list)
    for p, s in files:
        if s < 50_000:
            continue
        h = hashlib.md5()
        try:
            with p.open("rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    h.update(chunk)
            hashes[h.hexdigest()].append(p)
        except OSError:
            continue
    dups = {k: v for k, v in hashes.items() if len(v) > 1}
    dup_waste = sum(
        sum(p.stat().st_size for p in v[1:]) for v in dups.values()
    )

    # Reference scan: collect referenced paths from HTML/CSS/JS (sample of public+index)
    ref_roots = [ROOT / "index.html", PUBLIC]
    referenced: set[str] = set()
    ref_re = re.compile(
        r"""(?:src|href|poster|content|data-src|srcset)=["']([^"']+)["']|url\((['"]?)(/[^'")]+)\2\)""",
        re.I,
    )
    html_css_js = []
    if (ROOT / "index.html").exists():
        html_css_js.append(ROOT / "index.html")
    for folder in ("public",):
        root = ROOT / folder
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.suffix.lower() in {".html", ".css", ".js"} and p.is_file():
                html_css_js.append(p)

    for path in html_css_js:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in ref_re.finditer(text):
            raw = m.group(1) or m.group(3) or ""
            for part in raw.split(","):
                part = part.strip().split()[0] if part.strip() else ""
                if part.startswith("/") and not part.startswith("//"):
                    referenced.add(part.split("?")[0])

    # Unreferenced under media/ (candidates only)
    media_root = base / "media"
    unref = []
    if media_root.exists():
        for p, s in files:
            try:
                rel = "/" + p.relative_to(base).as_posix()
            except ValueError:
                continue
            if not rel.startswith("/media/"):
                continue
            if rel not in referenced:
                # also check basename soft match
                unref.append((rel, s))

    unref.sort(key=lambda x: x[1], reverse=True)

    def mb(n: int) -> str:
        return f"{n / 1024 / 1024:.1f} MB"

    lines = [
        "# Asset Audit",
        "",
        f"Base: `{base}`",
        f"Files: {len(files)}",
        f"Total: {mb(total)} ({total} bytes)",
        "",
        "## By category",
    ]
    for k in ("images", "videos", "fonts", "docs", "html", "css_js", "other"):
        lines.append(f"- {k}: {mb(by_cat[k])}")
    lines += ["", "## Top extensions"]
    for ext, s in sorted(by_ext.items(), key=lambda x: -x[1])[:20]:
        lines.append(f"- `{ext}`: {mb(s)}")
    lines += ["", "## 50 largest files"]
    for p, s in largest:
        rel = p.relative_to(base).as_posix()
        lines.append(f"- {mb(s)} — `{rel}`")
    lines += [
        "",
        f"## Duplicate files (>=50KB): groups={len(dups)} wasted≈{mb(dup_waste)}",
    ]
    shown = 0
    for digest, paths in sorted(dups.items(), key=lambda kv: -kv[1][0].stat().st_size):
        if shown >= 20:
            break
        sizes = paths[0].stat().st_size
        lines.append(f"- {mb(sizes)} ×{len(paths)} md5={digest[:10]}")
        for p in paths[:5]:
            lines.append(f"  - `{p.relative_to(base).as_posix()}`")
        shown += 1
    lines += [
        "",
        f"## Unreferenced /media candidates (path not seen in HTML/CSS/JS href/src): {len(unref)}",
        "NOTE: May still be used dynamically or from JSON. Do not delete blindly.",
        "",
    ]
    for rel, s in unref[:40]:
        lines.append(f"- {mb(s)} — `{rel}`")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"total {mb(total)} files {len(files)}")
    print("categories", {k: mb(by_cat[k]) for k in by_cat})
    print("dup_groups", len(dups), "dup_waste", mb(dup_waste))
    print("unref_media", len(unref), "top", unref[:5])


if __name__ == "__main__":
    main()
