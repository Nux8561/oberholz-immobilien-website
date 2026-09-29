from pathlib import Path

t = Path("index.html").read_text(encoding="utf-8", errors="replace")
# find Ute contexts
start = 0
n = 0
while n < 5:
    i = t.find("Ute Schorpp", start)
    if i < 0:
        break
    ctx = t[max(0, i - 120) : i + 140]
    Path("scripts/_ute_ctx.txt").write_text(ctx, encoding="utf-8")
    print("HIT", n, "len", len(ctx))
    # write all to file
    start = i + 1
    n += 1

# dump all ute snippets
out = []
start = 0
while True:
    i = t.find("Ute Schorpp", start)
    if i < 0:
        break
    out.append(t[max(0, i - 100) : i + 120])
    start = i + 1
Path("scripts/_ute_all.txt").write_text("\n---\n".join(out), encoding="utf-8")
print("ute hits index", len(out))

# facepile existence of oberholz
fp = Path("public/media/facepile")
print("files", [p.name for p in fp.iterdir()])
print("oberholz exists", (fp / "oberholz_facepile.jpg").exists())

# team JS dynamic for Ute?
for needle in ["teamImg", "Ute Schorpp", "Schorpp"]:
    print(needle, t.count(needle))
