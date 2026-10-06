# -*- coding: utf-8 -*-
"""Keep only /regionen/muenster/ as canonical; redirect munster variants."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MUNSTER = PUBLIC / "regionen" / "munster"
MUENSTER = PUBLIC / "regionen" / "muenster"

LINK_RE = re.compile(
    r"""(/regionen/)munster(/|\.html|["'?#])""",
    re.I,
)
CANONICAL_RE = re.compile(
    r"""(<link[^>]+rel=["']canonical["'][^>]*href=["'])([^"']+)(["'])""",
    re.I,
)


def ensure_muenster_pages() -> None:
    MUENSTER.mkdir(parents=True, exist_ok=True)
    if MUNSTER.exists():
        for src in MUNSTER.glob("*.html"):
            dst = MUENSTER / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
                print("copied missing", src.name, "-> muenster/", flush=True)


def patch_muenster_canonicals() -> int:
    changed = 0
    for path in MUENSTER.glob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        canon = f"/regionen/muenster/{path.name}"
        new = text
        # force canonical
        if CANONICAL_RE.search(new):
            new = CANONICAL_RE.sub(rf"\1{canon}\3", new, count=1)
        else:
            new = new.replace(
                "</head>",
                f'<link rel="canonical" href="{canon}"/>\n</head>',
                1,
            )
        # rewrite self munster refs
        new2, n = LINK_RE.subn(r"\1muenster\2", new)
        new = new2
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print("canonicalized", path.name, "ops", n, flush=True)
    return changed


def rewrite_internal_links() -> int:
    changed = 0
    files = [ROOT / "index.html"] + list(PUBLIC.rglob("*.html"))
    for path in files:
        if "regionen/munster" in path.as_posix().replace("\\", "/"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "/regionen/munster" not in text and "/regionen/Munster" not in text:
            continue
        new, n = LINK_RE.subn(r"\1muenster\2", text)
        # also plain path forms
        new2 = new.replace("/regionen/munster/", "/regionen/muenster/")
        new2 = new2.replace("/regionen/munster\"", "/regionen/muenster\"")
        new2 = new2.replace("/regionen/munster'", "/regionen/muenster'")
        if new2 != text:
            path.write_text(new2, encoding="utf-8")
            changed += 1
    print("rewrote munster links in files", changed, flush=True)
    return changed


def remove_munster_dir() -> None:
    if MUNSTER.exists():
        shutil.rmtree(MUNSTER)
        print("removed public/regionen/munster", flush=True)


def write_redirects_snippet() -> str:
    return "\n".join(
        [
            "# Canonical Münster",
            "/regionen/munster  /regionen/muenster/immobilienmakler.html  301",
            "/regionen/munster/  /regionen/muenster/immobilienmakler.html  301",
            "/regionen/munster/*  /regionen/muenster/:splat  301",
            "",
            "# True 404s: rely on top-level 404.html (no SPA /* -> index.html)",
            "",
        ]
    )


def update_regionen_hub() -> None:
    path = PUBLIC / "regionen.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    new = text.replace("/regionen/munster/", "/regionen/muenster/")
    if new != text:
        path.write_text(new, encoding="utf-8")
        print("updated regionen.html hub links", flush=True)


def main() -> None:
    ensure_muenster_pages()
    patch_muenster_canonicals()
    rewrite_internal_links()
    update_regionen_hub()
    remove_munster_dir()
    snippet = write_redirects_snippet()
    (ROOT / "analysis" / "muenster-redirects.txt").parent.mkdir(exist_ok=True)
    (ROOT / "analysis" / "muenster-redirects.txt").write_text(snippet, encoding="utf-8")
    print("DONE canonical=/regionen/muenster/", flush=True)
    print(snippet)


if __name__ == "__main__":
    main()
