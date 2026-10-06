# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MU = Path(__file__).resolve().parents[1] / "public" / "regionen" / "muenster"
CANON_RE = re.compile(
    r"""(<link[^>]+rel=["']canonical["'][^>]*href=["'])([^"']+)(["'])""",
    re.I,
)
CANON_RE2 = re.compile(
    r"""(<link[^>]+href=["'])([^"']+)(["'][^>]*rel=["']canonical["'])""",
    re.I,
)


def main() -> None:
    print("munster_dir_exists", (MU.parent / "munster").exists())
    print("muenster_files", sorted(p.name for p in MU.glob("*.html")) if MU.exists() else None)
    for path in MU.glob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        canon = f"/regionen/muenster/{path.name}"
        m = CANON_RE.search(text) or CANON_RE2.search(text)
        print(path.name, "before", m.group(2) if m else "MISSING")
        if m and m.group(2) == canon:
            continue
        if CANON_RE.search(text):
            text = CANON_RE.sub(rf"\1{canon}\3", text, count=1)
        elif CANON_RE2.search(text):
            text = CANON_RE2.sub(rf"\1{canon}\3", text, count=1)
        else:
            text = text.replace("</head>", f'<link rel="canonical" href="{canon}"/>\n</head>', 1)
        path.write_text(text, encoding="utf-8")
        print("fixed", path.name, "->", canon)


if __name__ == "__main__":
    main()
