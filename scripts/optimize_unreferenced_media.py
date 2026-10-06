# -*- coding: utf-8 -*-
"""
Remove only clearly unused template media / unreferenced duplicate copies.
Never touches referenced immobilien/logo/customer assets.
"""
from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MEDIA = PUBLIC / "media"
REPORT = ROOT / "analysis" / "asset-optimizations.md"

# Hard allowlist of obvious old-template leftovers (deleted only if unreferenced)
TEMPLATE_NAMES = {
    "munz_ie.png",
    "broschuere_ee-experten_web.pdf",
    "broschuere_ee-immobilien_web.pdf",
    "ie_logo.png",  # only if unreferenced; oberholz-logo is used
}


def collect_references() -> set[str]:
    refs: set[str] = set()
    pat = re.compile(
        r"""(?:src|href|poster|content|data-src)=["']([^"']+)["']|url\((['"]?)([^'")]+)\2\)""",
        re.I,
    )
    files = [ROOT / "index.html"]
    for folder in (PUBLIC,):
        for p in folder.rglob("*"):
            if p.suffix.lower() in {".html", ".css", ".js"} and p.is_file():
                files.append(p)
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in pat.finditer(text):
            raw = m.group(1) or m.group(3) or ""
            for chunk in raw.split(","):
                part = chunk.strip().split()[0] if chunk.strip() else ""
                if not part.startswith("/") or part.startswith("//"):
                    continue
                refs.add(part.split("?")[0])
                # also basename soft refs
                refs.add(Path(part.split("?")[0]).name)
    return refs


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    refs = collect_references()
    removed: list[tuple[str, int, str]] = []
    saved = 0

    # 1) Named template leftovers
    for name in sorted(TEMPLATE_NAMES):
        path = MEDIA / name
        if not path.is_file():
            continue
        rel = "/media/" + name
        if rel in refs or name in refs:
            print("keep referenced template-ish", rel, flush=True)
            continue
        size = path.stat().st_size
        path.unlink()
        removed.append((rel, size, "unreferenced template name"))
        saved += size
        print("removed", rel, size, flush=True)

    # 2) Duplicate copies: keep one referenced path; delete unreferenced identical copies >=100KB
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in MEDIA.rglob("*"):
        if not path.is_file():
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size < 100_000:
            continue
        try:
            by_hash[md5_file(path)].append(path)
        except OSError:
            continue

    for digest, paths in by_hash.items():
        if len(paths) < 2:
            continue
        referenced_paths = []
        unreferenced_paths = []
        for p in paths:
            rel = "/" + p.relative_to(PUBLIC).as_posix()
            if rel in refs or p.name in refs:
                referenced_paths.append(p)
            else:
                unreferenced_paths.append(p)
        # Only delete unreferenced duplicates when at least one referenced copy remains
        if not referenced_paths:
            continue
        for p in unreferenced_paths:
            rel = "/" + p.relative_to(PUBLIC).as_posix()
            size = p.stat().st_size
            p.unlink()
            removed.append((rel, size, f"unreferenced duplicate of {digest[:10]}"))
            saved += size
            print("removed dup", rel, flush=True)

    lines = [
        "# Asset optimizations applied",
        "",
        f"Saved bytes: {saved} ({saved/1024/1024:.1f} MB)",
        f"Removed files: {len(removed)}",
        "",
    ]
    for rel, size, reason in removed[:200]:
        lines.append(f"- {size/1024/1024:.2f} MB `{rel}` — {reason}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("DONE saved_mb", round(saved / 1024 / 1024, 1), "files", len(removed), flush=True)


if __name__ == "__main__":
    main()
