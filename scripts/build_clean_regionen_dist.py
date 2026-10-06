# -*- coding: utf-8 -*-
"""Build a minimal dist-regionen with only Bochum/Essen/Münster (overwrite old SEO dump)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "regionen"
DST = ROOT / "dist-regionen"
MAIN = "https://oberholz-immobilien.pages.dev"


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir()
    shutil.copytree(SRC, DST / "regionen")
    (DST / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0;url={MAIN}/regionen.html" />
  <title>Regionen</title>
</head>
<body>
  <p><a href="{MAIN}/regionen.html">Zu den Regionen</a></p>
</body>
</html>
""",
        encoding="utf-8",
    )
    shutil.copy2(ROOT / "public" / "404.html", DST / "404.html")
    for name in ("theme", "assets", "mediatypes", "images"):
        src = ROOT / "dist" / name
        if src.exists():
            print("copy", name, flush=True)
            shutil.copytree(src, DST / name)
    html = sum(1 for _ in DST.rglob("*.html"))
    dirs = sorted(p.name for p in (DST / "regionen").iterdir() if p.is_dir())
    print("dist-regionen html", html, "dirs", dirs, flush=True)


if __name__ == "__main__":
    main()
