"""Fast name/role patch: only HTML files that still contain old people names."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRED = (
    (re.compile(r"Kersten Streit", re.I), "Michael Oberholz"),
    (re.compile(r"Wolfgang Mayer", re.I), "Felix Lesch"),
    (re.compile(r"Axel Winkler", re.I), "Michael Penn"),
    (re.compile(r"Ren(?:é|&eacute;|&#233;) Mohr", re.I), "Pascal Kopp"),
    (re.compile(r"Christian Munz", re.I), "Lubka Röger"),
    (re.compile(r"Gebietsleiter(?:in)? Immobilienverkauf", re.I), "Immobilienberater"),
    (re.compile(r"Leitung Immobilienverkauf", re.I), "Inhaber &amp; Sachverständiger"),
    (re.compile(r"Leitung Immobilienvermittlung", re.I), "Inhaber &amp; Sachverständiger"),
    (re.compile(r"Leiter Immobilienverkauf", re.I), "Inhaber &amp; Sachverständiger"),
    (re.compile(r"streit_facepile\.jpg"), "oberholz_facepile.jpg"),
)


def candidate_files() -> list[Path]:
    pattern = (
        "Wolfgang Mayer|Kersten Streit|Axel Winkler|Christian Munz|"
        "René Mohr|Rene Mohr|Ren&eacute; Mohr|"
        "Gebietsleiter Immobilienverkauf|Gebietsleiterin Immobilienverkauf|"
        "Leiter Immobilienverkauf|Leitung Immobilienverkauf|"
        "Leitung Immobilienvermittlung|streit_facepile"
    )
    proc = subprocess.run(
        [
            "rg",
            "-l",
            "--glob",
            "*.html",
            "--glob",
            "!node_modules/**",
            "--glob",
            "!dist/**",
            pattern,
            str(ROOT),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    files = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        path = Path(line)
        if "assets" in path.parts and path.name.startswith("_"):
            continue
        files.append(path)
    return files


def main() -> None:
    files = candidate_files()
    print("candidates", len(files))
    changed = 0
    subs = 0
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text
        for pattern, repl in PAIRED:
            text, n = pattern.subn(repl, text)
            subs += n
        text = text.replace(
            "Lubka Röger - Immobilienberater",
            "Lubka Röger - Immobilienberaterin",
        )
        text = text.replace(
            "Lubka Röger – Immobilienberater",
            "Lubka Röger – Immobilienberaterin",
        )
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print("html files changed", changed, "substitutions", subs)


if __name__ == "__main__":
    main()
