# -*- coding: utf-8 -*-
"""Remove template SEO city pages; keep Bochum/Essen/Münster + all Immobilien."""
from __future__ import annotations

import re
import shutil
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
REGIONEN = PUBLIC / "regionen"
KONTAKT = PUBLIC / "kontakt"
ANALYSIS = ROOT / "analysis"
IMMOBILIEN = PUBLIC / "immobilien"

KEEP_REGION_DIRS = {"bochum", "essen", "muenster", "munster"}
KEEP_KONTAKT_NAMES = {
    "immobilienmakler-bochum.html",
    "immobilienmakler-essen.html",
    "immobilienmakler-muenster.html",
    "kontakt-aufnehmen.html",
    "immobilienmakler-bochum",
    "immobilienmakler-essen",
    "immobilienmakler-muenster",
}

# kontakt city slugs that stay
KEEP_KONTAKT_SLUGS = {"bochum", "essen", "muenster"}

FOREIGN_KONTAKT_RE = re.compile(
    r"""(/kontakt/immobilienmakler-(?!bochum|essen|muenster)[a-z0-9\-]+)(?:\.html)?""",
    re.I,
)
FOREIGN_REGION_RE = re.compile(
    r"""(/regionen/(?!bochum|essen|muenster|munster)(?:/|(?=["'\s?#])))""",
    re.I,
)
# Full path match for regionen foreign cities
REGION_HREF_RE = re.compile(
    r"""href=(["'])(/regionen/(?!bochum(?:/|"|'|\?)|essen(?:/|"|'|\?)|muenster(?:/|"|'|\?)|munster(?:/|"|'|\?))[^"']*)\1""",
    re.I,
)
KONTAKT_HREF_RE = re.compile(
    r"""href=(["'])(/kontakt/immobilienmakler-(?!bochum|essen|muenster)[^"']*)\1""",
    re.I,
)


def count_html(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.rglob("*.html"))


def delete_foreign_regionen() -> tuple[int, int, list[str]]:
    removed_dirs = 0
    removed_files = 0
    urls: list[str] = []
    if not REGIONEN.exists():
        return 0, 0, urls

    for entry in sorted(REGIONEN.iterdir(), key=lambda p: p.name):
        name = entry.name
        if entry.is_dir():
            if name.lower() in KEEP_REGION_DIRS:
                continue
            # count html before delete
            htmls = list(entry.rglob("*.html"))
            for h in htmls:
                rel = h.relative_to(PUBLIC).as_posix()
                urls.append("/" + rel)
            removed_files += len(htmls)
            shutil.rmtree(entry, ignore_errors=True)
            removed_dirs += 1
            if removed_dirs % 500 == 0:
                print(f"  ... removed {removed_dirs} region dirs", flush=True)
        elif entry.is_file() and entry.suffix.lower() == ".html":
            # letter indexes / orphan pages under /regionen/
            urls.append("/regionen/" + name)
            entry.unlink(missing_ok=True)
            removed_files += 1
    return removed_dirs, removed_files, urls


def delete_foreign_kontakt() -> tuple[int, list[str]]:
    removed = 0
    urls: list[str] = []
    if not KONTAKT.exists():
        return 0, urls
    for entry in list(KONTAKT.iterdir()):
        if entry.name in KEEP_KONTAKT_NAMES:
            continue
        if entry.is_dir():
            htmls = list(entry.rglob("*.html"))
            for h in htmls:
                urls.append("/" + h.relative_to(PUBLIC).as_posix())
            shutil.rmtree(entry, ignore_errors=True)
            removed += 1
        elif entry.is_file():
            urls.append("/kontakt/" + entry.name)
            entry.unlink(missing_ok=True)
            removed += 1
    return removed, urls


def rewrite_regionen_overview() -> None:
    """Replace bloated regionen.html with a short 3-city hub (same theme chrome if possible)."""
    path = PUBLIC / "regionen.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")

    # Try to keep head + header/footer by swapping only main content block
    cities = [
        ("Bochum", "/regionen/bochum/immobilienmakler.html", "/regionen/bochum/immobilie-verkaufen.html"),
        ("Essen", "/regionen/essen/immobilienmakler.html", "/regionen/essen/immobilie-verkaufen.html"),
        ("Münster", "/regionen/muenster/immobilienmakler.html", "/regionen/muenster/immobilie-verkaufen.html"),
    ]
    cards = []
    for name, makler, verkauf in cities:
        cards.append(
            f"""
            <div class="col-md-4 mb-4">
              <div class="regio-prozess-card">
                <h2 class="h4 mb-3">{name}</h2>
                <p class="mb-3">Ihr Immobilienmakler vor Ort – Beratung, Verkauf und Wertermittlung.</p>
                <p class="mb-2"><a href="{makler}">Immobilienmakler {name}</a></p>
                <p class="mb-0"><a href="{verkauf}">Immobilie verkaufen in {name}</a></p>
              </div>
            </div>"""
        )
    block = f"""
<section class="py-5">
  <div class="container">
    <h1 class="mb-3">Unsere Regionen</h1>
    <p class="lead mb-4">Oberholz Immobilien ist aktiv in Bochum, Essen und Münster.</p>
    <div class="row">{"".join(cards)}
    </div>
  </div>
</section>
"""

    # Prefer replacing <main>...</main> or content between hero and footer
    main_re = re.compile(r"<main\b[^>]*>.*?</main>", re.I | re.S)
    if main_re.search(text):
        text = main_re.sub(f"<main id=\"content\">{block}</main>", text, count=1)
    else:
        # Insert before footer if present
        footer_re = re.compile(r"(<footer\b)", re.I)
        if footer_re.search(text):
            # Remove old regio listing sections that contain many /regionen/ links
            # Drop dense link clouds: replace body content between body and footer roughly
            body_open = re.search(r"<body\b[^>]*>", text, re.I)
            footer_m = footer_re.search(text)
            if body_open and footer_m and footer_m.start() > body_open.end():
                head = text[: body_open.end()]
                # keep header-ish first 80k max if it looks like nav
                prefix = text[body_open.end() : footer_m.start()]
                # Keep only header/nav snippet if present
                nav_keep = ""
                nav_m = re.search(
                    r"(<header\b.*?</header>|<nav\b.*?id=\"navbarmain\".*?</nav>)",
                    prefix,
                    re.I | re.S,
                )
                if nav_m:
                    nav_keep = nav_m.group(1)
                text = head + nav_keep + block + text[footer_m.start() :]
        else:
            # fallback: write minimal page using existing head
            head_m = re.search(r"(.*?</head>\s*<body\b[^>]*>)", text, re.I | re.S)
            if head_m:
                text = (
                    head_m.group(1)
                    + block
                    + '<p class="container py-3"><a href="/">Zur Startseite</a></p></body></html>'
                )

    # Meta cleanup
    text = re.sub(
        r"<title>[^<]*</title>",
        "<title>Regionen | Bochum, Essen, Münster – Oberholz Immobilien</title>",
        text,
        count=1,
        flags=re.I,
    )
    text = re.sub(
        r'property="og:title" content="[^"]*"',
        'property="og:title" content="Regionen | Bochum, Essen, Münster – Oberholz Immobilien"',
        text,
        count=1,
        flags=re.I,
    )
    path.write_text(text, encoding="utf-8")
    print("rewrote regionen.html", flush=True)


def patch_html_links(text: str) -> tuple[str, int]:
    ops = 0

    def repl_region(m: re.Match[str]) -> str:
        nonlocal ops
        ops += 1
        quote = m.group(1)
        return f"href={quote}/regionen.html{quote}"

    def repl_kontakt(m: re.Match[str]) -> str:
        nonlocal ops
        ops += 1
        quote = m.group(1)
        return f"href={quote}/kontakt/kontakt-aufnehmen.html{quote}"

    new = REGION_HREF_RE.sub(repl_region, text)
    new = KONTAKT_HREF_RE.sub(repl_kontakt, new)

    # Plain mentions in meta that point to foreign kontakt cities
    new2, n = FOREIGN_KONTAKT_RE.subn("/kontakt/kontakt-aufnehmen.html", new)
    ops += n
    new = new2
    return new, ops


def patch_remaining_html() -> tuple[int, int]:
    changed = 0
    ops_total = 0
    skip_parts = {".git", "node_modules", "dist", "dist-regionen", "reference", "screenshots"}
    roots = [ROOT / "index.html", PUBLIC]
    files: list[Path] = []
    if (ROOT / "index.html").exists():
        files.append(ROOT / "index.html")
    for p in PUBLIC.rglob("*.html"):
        # skip nothing under immobilien for deletion, but DO patch links
        files.append(p)

    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "/regionen/" not in raw and "/kontakt/immobilienmakler-" not in raw:
            # still may have foreign kontakt
            if "immobilienmakler-duesseldorf" not in raw and "immobilienmakler-hamburg" not in raw:
                if "immobilienmakler-muenchen" not in raw and "immobilienmakler-frankfurt" not in raw:
                    if "immobilienmakler-stuttgart" not in raw and "immobilienmakler-hannover" not in raw:
                        if "immobilienmakler-villingen" not in raw:
                            continue
        new, ops = patch_html_links(raw)
        if ops and new != raw:
            path.write_text(new, encoding="utf-8")
            changed += 1
            ops_total += ops
    return changed, ops_total


def write_redirect_doc(urls: list[str]) -> None:
    ANALYSIS.mkdir(exist_ok=True)
    out = ANALYSIS / "removed-region-urls.md"
    lines = [
        "# Entfernte Template-Orts-/Regions-URLs",
        "",
        "Aktive Regionen: Bochum, Essen, Münster.",
        "Immobilienobjekte wurden nicht gelöscht.",
        "",
        "Empfehlung später (nicht automatisch gesetzt): 301 → `/` oder passende Stadtseite.",
        "",
        f"Anzahl: {len(urls)}",
        "",
    ]
    # store a sample + full list in companion txt to keep md readable
    sample = urls[:200]
    lines.append("## Stichprobe (erste 200)")
    lines.extend(f"- `{u}`" for u in sample)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ANALYSIS / "removed-region-urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    print("wrote", out, "and removed-region-urls.txt", flush=True)


def main() -> None:
    start = time.time()
    immo_before = count_html(IMMOBILIEN)
    reg_before = count_html(REGIONEN)
    kontakt_before = count_html(KONTAKT)
    print(
        f"BEFORE immobilien={immo_before} regionen={reg_before} kontakt={kontakt_before}",
        flush=True,
    )

    print("Deleting foreign regionen…", flush=True)
    rd, rf, urls_r = delete_foreign_regionen()
    print(f"Removed region dirs={rd} html_files≈{rf}", flush=True)

    print("Deleting foreign kontakt…", flush=True)
    kd, urls_k = delete_foreign_kontakt()
    print(f"Removed kontakt entries={kd}", flush=True)

    urls = urls_r + urls_k
    write_redirect_doc(urls)

    print("Rewriting regionen overview…", flush=True)
    rewrite_regionen_overview()

    print("Patching remaining HTML links…", flush=True)
    changed, ops = patch_remaining_html()
    print(f"Patched files={changed} link_ops={ops}", flush=True)

    immo_after = count_html(IMMOBILIEN)
    reg_after = count_html(REGIONEN)
    kontakt_after = count_html(KONTAKT)
    print(
        f"AFTER immobilien={immo_after} regionen={reg_after} kontakt={kontakt_after}",
        flush=True,
    )
    if immo_after != immo_before:
        print("ERROR: immobilien count changed!", flush=True)
        sys.exit(2)

    kept = sorted(p.name for p in REGIONEN.iterdir() if p.is_dir()) if REGIONEN.exists() else []
    print("Kept region dirs:", kept, flush=True)
    print(f"DONE in {time.time()-start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
