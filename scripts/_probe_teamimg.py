from pathlib import Path

t = Path("index.html").read_text(encoding="utf-8", errors="replace")
# extract teamImg assignment
for needle in ["var teamImg", "teamImg =", "teamImg="]:
    i = t.find(needle)
    if i >= 0:
        Path("scripts/_teamimg.txt").write_text(t[i : i + 200], encoding="utf-8")
        print("found", needle, "at", i)

# also search profilbild in index
idxs = []
start = 0
while True:
    i = t.find("profilbild", start)
    if i < 0:
        break
    idxs.append(t[max(0, i - 40) : i + 80])
    start = i + 1
Path("scripts/_profilbild_refs.txt").write_text("\n---\n".join(idxs[:20]), encoding="utf-8")
print("profilbild refs", len(idxs))
