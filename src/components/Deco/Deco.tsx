import './Deco.css';

/* Dekor: Giebelzeile nach Vorbild des Münsteraner Prinzipalmarkts als feine Linie, Formensprache
   „Fuge & Raute“ (brand/README.md): Giebel, Wände, Gesims und Bögen berühren sich nicht, Punkte sind Rauten.
   Fläche 2828 × 250, eine Einheit = 1 px (die Grafik wird nur beschnitten, nie skaliert). */
const W = 2828;
const G = 250; // Unterkante: Wände und Bögen laufen bis zum Rand
const F = 5; // Fuge zwischen Bauteilen
const GAP = 7; // Fuge zwischen zwei Häusern

type Pt = [number, number];
type Seg = { p: Pt; c?: Pt };
type House = { x: number; w: number; eave: number; h: number; kind: 'stufen' | 'spitz' | 'schweif' | 'rathaus' | 'turm'; accent: boolean };

const r1 = (n: number) => Math.round(n * 10) / 10;
const pt = ([x, y]: Pt) => `${r1(x)} ${r1(y)}`;
const raute = (cx: number, cy: number, r: number) => `M${r1(cx)} ${r1(cy - r)}l${r} ${r}-${r} ${r}-${r}-${r}Z`;

// feste Zufallsfolge, damit die Zeile bei jedem Laden gleich aussieht
let seed = 11;
const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const between = (a: number, b: number) => Math.round(a + rnd() * (b - a));

/** Symmetrischer Umriss: linke Hälfte von der Traufe bis zur Mitte, rechte Hälfte gespiegelt */
function mirrored(cx: number, p0: Pt, segs: Seg[]) {
  const m = ([x, y]: Pt): Pt => [2 * cx - x, y];
  const pts = [p0, ...segs.map((s) => s.p)];
  let d = `M${pt(p0)}` + segs.map((s) => (s.c ? `Q${pt(s.c)} ${pt(s.p)}` : `L${pt(s.p)}`)).join('');
  const last = pts[pts.length - 1];
  if (Math.abs(last[0] - cx) > 0.05) d += `L${pt(m(last))}`;
  for (let i = segs.length - 1; i >= 0; i--) {
    const s = segs[i];
    d += s.c ? `Q${pt(m(s.c))} ${pt(m(pts[i]))}` : `L${pt(m(pts[i]))}`;
  }
  return d;
}

/** Treppengiebel: n Stufen je Seite, oben ein schmaler Abschluss */
function stufen(x: number, w: number, b: number, h: number, n: number) {
  const cx = x + w / 2, cap = w * 0.16, sw = (w / 2 - cap / 2) / n, sh = h / (n + 0.7);
  const segs: Seg[] = [];
  for (let i = 0; i < n; i++) segs.push({ p: [x + i * sw, b - (i + 1) * sh] }, { p: [x + (i + 1) * sw, b - (i + 1) * sh] });
  segs.push({ p: [cx - cap / 2, b - h] });
  return { d: mirrored(cx, [x, b], segs), sw, sh };
}

/** Schweifgiebel: zwei geschwungene Schultern, runder Abschluss */
function schweif(x: number, w: number, b: number, h: number) {
  const cx = x + w / 2;
  return mirrored(cx, [x, b], [
    { p: [x, b - 0.1 * h] },
    { c: [x, b - 0.4 * h], p: [x + 0.15 * w, b - 0.4 * h] },
    { p: [x + 0.15 * w, b - 0.52 * h] },
    { c: [x + 0.15 * w, b - 0.8 * h], p: [x + 0.31 * w, b - 0.8 * h] },
    { p: [x + 0.31 * w, b - 0.86 * h] },
    { c: [x + 0.31 * w, b - h], p: [cx, b - h] },
  ]);
}

// Häuserzeile: Breiten, Traufhöhen und Giebelformen wechseln; Rathaus und Kirchturm stehen nahe der Mitte,
// damit sie auch im schmalen Ausschnitt (Mobil) sichtbar sind.
const HOUSES: House[] = [];
{
  const kinds: House['kind'][] = ['stufen', 'schweif', 'spitz', 'stufen', 'schweif', 'stufen', 'spitz'];
  let x = 4, k = 0, rathaus = false, turm = false;
  while (x < W) {
    if (!rathaus && x > 1180) {
      HOUSES.push({ x, w: 112, eave: 126, h: 90, kind: 'rathaus', accent: false });
      x += 112 + GAP; rathaus = true; continue;
    }
    if (!turm && x > 1470) {
      HOUSES.push({ x, w: 46, eave: 104, h: 80, kind: 'turm', accent: true });
      x += 46 + GAP; turm = true; continue;
    }
    const w = between(62, 98);
    const kind = kinds[k++ % kinds.length];
    HOUSES.push({ x, w, eave: between(116, 146), h: kind === 'spitz' ? between(48, 62) : between(58, 78), kind, accent: k % 5 === 2 });
    x += w + GAP;
  }
}

const LINES: string[] = []; // Umrisse
const DETAIL: string[] = []; // Fenster, Gesims, Bögen
const RAUTEN: string[] = [];
const AKZENT: string[] = [];

/** Bogengang im Erdgeschoss: k Bögen zwischen den Wänden, mit Fuge zu Wand und Nachbarbogen */
function arcade(x: number, w: number, k: number, top: number) {
  const inner = w - 2 * (F + 3), aw = (inner - (k - 1) * (F + 3)) / k, r = aw / 2;
  for (let j = 0; j < k; j++) {
    const ax = x + F + 3 + j * (aw + F + 3);
    DETAIL.push(`M${r1(ax)} ${G}V${r1(top + r)}a${r1(r)} ${r1(r)} 0 0 1 ${r1(aw)} 0V${G}`);
  }
}

/** Fensterachsen: jedes Fenster als zwei Laibungen */
function windows(x: number, w: number, from: number, to: number) {
  const cols = w < 76 ? 2 : 3, floors = Math.max(1, Math.round((to - from) / 34)), fh = (to - from) / floors;
  for (let f = 0; f < floors; f++) {
    const y = from + f * fh + fh * 0.22, wh = fh * 0.52;
    for (let c = 0; c < cols; c++) {
      const cx = x + (w * (c + 0.5)) / cols;
      DETAIL.push(`M${r1(cx - 4)} ${r1(y)}v${r1(wh)}M${r1(cx + 4)} ${r1(y)}v${r1(wh)}`);
    }
  }
}

for (const { x, w, eave, h, kind, accent } of HOUSES) {
  const cx = x + w / 2, b = eave - F, top = b - h;
  const gesims = G - 56; // Oberkante Bogengang

  // Wände und Gesims (Gesims mit Fuge zu den Wänden)
  LINES.push(`M${x} ${G}V${eave}M${x + w} ${G}V${eave}`);
  DETAIL.push(`M${x + F} ${gesims}H${x + w - F}`);

  if (kind === 'turm') {
    // Kirchturm: schlanker Helm mit Raute als Spitze, Uhr, Schallöffnung und Portal
    LINES.push(`M${x - 3} ${b}L${cx} ${top}L${x + w + 3} ${b}`);
    RAUTEN.push(raute(cx, eave + 20, 3));
    DETAIL.push(`M${x + F} ${eave + 40}H${x + w - F}`);
    DETAIL.push(`M${cx - 5} ${eave + 48}v36M${cx + 5} ${eave + 48}v36`);
    arcade(x, w, 1, gesims + F);
    AKZENT.push(raute(cx, top - F - 4, 4));
    continue;
  }

  if (kind === 'rathaus') {
    // Rathaus: hoher Treppengiebel mit Fialen auf jeder Stufe
    const n = 4, { d, sw, sh } = stufen(x, w, b, h, n);
    LINES.push(d);
    for (let i = 0; i < n; i++) {
      const y = b - (i + 1) * sh - F;
      for (const px of [x + i * sw + sw * 0.5, x + w - i * sw - sw * 0.5]) {
        DETAIL.push(`M${r1(px)} ${r1(y)}v-12`);
        RAUTEN.push(raute(px, y - 12 - F - 2, 2));
      }
    }
    DETAIL.push(`M${cx} ${r1(top - F)}v-12`);
    RAUTEN.push(raute(cx, top - F - 12 - F - 3, 3));
    DETAIL.push(`M${r1(x + w * 0.3)} ${r1(b - h * 0.3)}v14M${r1(x + w * 0.7)} ${r1(b - h * 0.3)}v14`);
    RAUTEN.push(raute(cx, b - h * 0.55, 3));
    windows(x, w, eave + F, gesims - F);
    arcade(x, w, 3, gesims + F);
    continue;
  }

  if (kind === 'stufen') LINES.push(stufen(x, w, b, h, w < 76 ? 3 : 4).d);
  else if (kind === 'schweif') LINES.push(schweif(x, w, b, h));
  else LINES.push(`M${x} ${b}L${cx} ${top}L${x + w} ${b}`);

  // Giebelfenster als Raute, vereinzelt in Akzentfarbe
  (accent ? AKZENT : RAUTEN).push(raute(cx, b - h * (kind === 'spitz' ? 0.38 : 0.45), 3.5));
  windows(x, w, eave + F, gesims - F);
  arcade(x, w, w < 76 ? 1 : 2, gesims + F);
}

const PATHS = { lines: LINES.join(''), detail: DETAIL.join(''), rauten: RAUTEN.join(''), akzent: AKZENT.join('') };

export default function Deco({ className = '' }: { className?: string }) {
  return (
    <div className="deco-wrap" aria-hidden="true">
    <svg className={`deco ${className}`} viewBox="0 0 2828 250" preserveAspectRatio="xMidYMax slice">
      <path className="deco__detail" d={PATHS.detail} />
      <path className="deco__line" d={PATHS.lines} />
      <path className="deco__raute" d={PATHS.rauten} />
      <path className="deco__akzent" d={PATHS.akzent} />
    </svg>
    </div>
  );
}
