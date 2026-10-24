// Exportiert das Oberholz-Icon-Set aus src/icons/pack.ts nach brand/icons/
// (Einzel-SVGs + Sprite). Aufruf: node scripts/export_icons.ts  (Node ≥ 22.18, TS-Typen werden ignoriert)
import { mkdirSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ICONS, type IconDef } from '../src/icons/pack.ts';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'brand', 'icons');
const SVG_DIR = join(OUT, 'svg');

const inner = (d: IconDef) =>
  (d.s ? `<path d="${d.s}"/>` : '')
  + (d.f ? `<path d="${d.f}" fill="currentColor" stroke="none"/>` : '')
  + (d.a ? `<path class="oi-a" d="${d.a}" style="fill:var(--oi-accent,currentColor)" stroke="none"/>` : '');

const attrs = 'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="butt" stroke-linejoin="miter"';

mkdirSync(SVG_DIR, { recursive: true });
for (const f of readdirSync(SVG_DIR)) rmSync(join(SVG_DIR, f));

const symbols: string[] = [];
for (const [name, def] of Object.entries(ICONS) as [string, IconDef][]) {
  const [w, h] = def.vb ?? [24, 24];
  writeFileSync(
    join(SVG_DIR, `${name}.svg`),
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" ${attrs}>`
      + `<title>${def.t} – Oberholz Icons</title>${inner(def)}</svg>\n`,
  );
  symbols.push(`<symbol id="oi-${name}" viewBox="0 0 ${w} ${h}" ${attrs}><title>${def.t}</title>${inner(def)}</symbol>`);
}
writeFileSync(
  join(OUT, 'sprite.svg'),
  `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n<!-- Oberholz Icons © 2026 Oberholz Immobilien -->\n${symbols.join('\n')}\n</svg>\n`,
);
console.log(`${symbols.length} Icons → brand/icons/svg/*.svg + brand/icons/sprite.svg`);

/* ---------- Markenhandbuch brand/index.html (Schriften + Icons auf einen Blick) ---------- */
const cell = ([name, def]: [string, IconDef]) => {
  const [w, h] = def.vb ?? [24, 24];
  const big = w > 24;
  const svg = (px: number) =>
    `<svg width="${px}" height="${Math.round((px * h) / w)}" viewBox="0 0 ${w} ${h}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="butt" stroke-linejoin="miter">`
    + inner(def).replace(/<path d=/, '<path vector-effect="non-scaling-stroke" d=') + '</svg>';
  return `<figure class="ic${big ? ' ic--big' : ''}"><div>${big ? svg(w > 48 ? 120 : 96) : svg(24) + svg(48)}</div>`
    + `<figcaption><b>${name}</b>${def.t}</figcaption></figure>`;
};
const entries = Object.entries(ICONS) as [string, IconDef][];
const html = `<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Oberholz Markenhandbuch</title>
<style>
@font-face{font-family:'Oberholz Antiqua';font-weight:600;src:url(fonts/oberholz-antiqua-600-latin.woff2) format('woff2')}
${[400, 500, 600, 700].map((wt) => `@font-face{font-family:'Oberholz Grotesk';font-weight:${wt};src:url(fonts/oberholz-grotesk-${wt}-latin.woff2) format('woff2')}`).join('\n')}
:root{--ink:#0d0d0d;--text:#404040;--muted:#666;--line:#e8e8e8;--cream:#fcfaf5;--oi-accent:#e60000}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--text);font:400 16px/1.6 'Oberholz Grotesk',Arial,sans-serif;letter-spacing:.3px}
main{max-width:1128px;margin:0 auto;padding:56px 16px 96px}
h1,h2,.ant{font-family:'Oberholz Antiqua',Georgia,serif;font-weight:600;color:var(--ink);letter-spacing:-.01em}
h1{font-size:clamp(36px,6vw,64px);line-height:1.1;margin:0 0 16px}h2{font-size:28px;line-height:1.3;margin:72px 0 8px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--ink)}
.lead{max-width:44em;font-size:18px}hr{border:0;border-top:2px solid var(--oi-accent);width:48px;margin:24px 0}
.spec{border:1px solid var(--line);padding:32px;margin-top:24px;background:var(--cream)}
.spec .big{font-size:clamp(40px,8vw,88px);line-height:1.05;color:var(--ink)}.spec p{margin:8px 0 0}
.meta{font-size:13px;color:var(--muted);margin-top:16px}
.w{display:flex;flex-wrap:wrap;gap:24px;margin-top:12px;font-size:22px;color:var(--ink)}
ul.rules{padding-left:20px;max-width:46em}ul.rules li{margin:6px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:24px}
.ic{margin:0;border:1px solid var(--line);padding:16px;color:var(--ink)}.ic div{display:flex;align-items:flex-end;gap:16px;height:96px}
.ic--big{grid-column:span 2}.ic--big div{height:auto;min-height:96px}
figcaption{margin-top:12px;font-size:12px;line-height:1.4;color:var(--muted)}figcaption b{display:block;color:var(--ink);font-weight:600}
code{font-size:13px;background:#f3f3f3;padding:1px 5px}
</style></head><body><main>
<p class="eyebrow">Oberholz Immobilien · Markenhandbuch</p>
<h1>Schriften &amp; Icons</h1>
<hr>
<p class="lead">Eigene Hausschriften und ein eigenes Icon-Set für oberholz-immobilien.de. Gemeinsames Merkmal ist die <b>Raute</b>:
alle Punkte (i, j, Umlaute, Satzzeichen) und Akzente sind auf der Spitze stehende Quadrate.</p>

<h2>Oberholz Antiqua</h2>
<p>Überschriften · Schnitt 600 · Basis Spectral (SIL Open Font License 1.1)</p>
<div class="spec"><div class="big ant">Ihr Immobilienpartner für Münster</div>
<p class="ant" style="font-size:28px;color:var(--ink)">Äpfel, Öfen, Übergabe · Größe? Ja!</p>
<p class="meta">ABCDEFGHIJKLMNOPQRSTUVWXYZ ÄÖÜ · abcdefghijklmnopqrstuvwxyz äöüß · 0123456789 € &amp; „…“</p></div>

<h2>Oberholz Grotesk</h2>
<p>Fließtext, Navigation, Buttons · Schnitte 400 / 500 / 600 / 700 · Basis Inter Tight (SIL Open Font License 1.1)</p>
<div class="spec"><p style="font-size:18px;color:var(--ink);max-width:40em">Wir begleiten Sie persönlich: von der Wertermittlung über die Vermarktung bis zur Übergabe.
Fragen? Rufen Sie uns an – Mo–Fr, 9:00–18:00 Uhr.</p>
<div class="w"><span style="font-weight:400">Regular 400</span><span style="font-weight:500">Medium 500</span><span style="font-weight:600">SemiBold 600</span><span style="font-weight:700">Bold 700</span></div>
<p class="eyebrow" style="margin-top:20px">Immobilie verkaufen · Preis auf Anfrage</p></div>

<h2>Oberholz Icons</h2>
<p>${entries.length} Motive · Formensprache „Fuge &amp; Raute“</p>
<ul class="rules">
<li><b>Raster</b> 24 × 24 (Illustrationen 48 × 48), 2 Einheiten Schutzzone.</li>
<li><b>Linie</b> 1,5 px, stumpfe Enden, spitze Ecken – keine abgerundeten Rechtecke.</li>
<li><b>Fuge</b>: Bauteile berühren sich nicht – zwischen Dach und Wand, Glas und Griff bleibt Luft.</li>
<li><b>Raute</b>: Punkte und Akzente als Raute; in Inhaltsbereichen rot (<code>#e60000</code>), in Bedienelementen in Textfarbe.</li>
</ul>
<div class="grid">${entries.map(cell).join('')}</div>

<h2>Dateien &amp; Lizenz</h2>
<ul class="rules">
<li><code>fonts/*.woff2</code> – Webfonts (Latein + Latein erweitert), <code>fonts/OFL.txt</code> – Lizenz, <code>fonts/source/</code> – Grundschriften.</li>
<li><code>icons/svg/*.svg</code> – Einzel-Icons, <code>icons/sprite.svg</code> – alle als &lt;symbol id="oi-name"&gt;.</li>
<li>Quellen im Code: <code>src/icons/pack.ts</code> (Icons), <code>scripts/build_brand_fonts.py</code> (Schriften), <code>scripts/export_icons.ts</code> (dieser Export).</li>
<li>Icons: © 2026 Oberholz Immobilien, eigene Gestaltung. Schriften: Hausschnitte unter SIL Open Font License 1.1 (siehe README.md).</li>
</ul>
</main></body></html>
`;
writeFileSync(join(ROOT, 'brand', 'index.html'), html);
console.log('Markenhandbuch → brand/index.html');
