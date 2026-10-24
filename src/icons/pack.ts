/* Oberholz Icons – eigenes Icon-Set von Oberholz Immobilien (Formensprache „Fuge & Raute“).

   Regeln (siehe brand/README.md):
   • Raster 24 × 24 (Illustrationen 48 × 48), 2 Einheiten Schutzzone.
   • Linie 1,5 px, stumpfe Enden, spitze Ecken, keine Rundungen an Rechtecken.
   • Fuge: Bauteile berühren sich nicht – zwischen Dach und Wand, Glas und Griff usw. bleibt 1,5 Einheiten Luft.
   • Raute: Punkte und Akzente sind auf der Spitze stehende Quadrate (wie die Punkte der Hausschriften);
     sie übernehmen die Akzentfarbe (--oi-accent), sonst die Textfarbe.

   Diese Datei ist die einzige Quelle: Website (src/icons/Icon.tsx) und Export
   (scripts/export_icons.ts → brand/icons) lesen beide hier. Nur löschbare TS-Syntax verwenden. */

export type IconDef = {
  /** Linien (stroke) */
  s?: string;
  /** Flächen in Textfarbe */
  f?: string;
  /** Rauten-Akzente (Fläche in --oi-accent) */
  a?: string;
  /** viewBox-Größe, Standard 24 × 24 */
  vb?: [number, number];
  /** Kurzbeschreibung für das Markenhandbuch */
  t: string;
};

const r2 = (n: number) => Math.round(n * 100) / 100;
/** Kreis als Pfad */
export const circle = (cx: number, cy: number, r: number) =>
  `M${r2(cx - r)} ${cy}a${r} ${r} 0 1 0 ${r2(2 * r)} 0a${r} ${r} 0 1 0 ${r2(-2 * r)} 0Z`;
/** Raute (auf der Spitze stehendes Quadrat), r = halbe Diagonale */
export const raute = (cx: number, cy: number, r: number) =>
  `M${cx} ${r2(cy - r)}l${r} ${r}-${r} ${r}-${r}-${r}Z`;
/** Strecke a→b, an beiden Enden um `gap` gekürzt (Fuge zu den Eckpunkten) */
const seg = (ax: number, ay: number, bx: number, by: number, gap: number) => {
  const len = Math.hypot(bx - ax, by - ay);
  const ux = ((bx - ax) / len) * gap, uy = ((by - ay) / len) * gap;
  return `M${r2(ax + ux)} ${r2(ay + uy)}L${r2(bx - ux)} ${r2(by - uy)}`;
};

const PIN = 'M12 2.5l7.25 6V14L12 21.5 4.75 14V8.5Z';
const PHONE = 'M8.5 3.5H4.25a.75.75 0 0 0-.75.75C3.5 13.5 10.5 20.5 19.75 20.5a.75.75 0 0 0 .75-.75V15.5l-4.5-1.5-2.25 2.25a12 12 0 0 1-6-6L10 8Z';
const GLOBE = circle(12, 12, 9) + 'M4.5 12h15M12 3c-2.5 2.5-3.75 5.5-3.75 9s1.25 6.5 3.75 9c2.5-2.5 3.75-5.5 3.75-9S14.5 5.5 12 3Z';
// Grundstück: vier Grenzsteine (Rauten), Grenzlinien mit Fuge
const PLOT: [number, number][] = [[4, 19.5], [7, 4.5], [20, 4.5], [17.5, 19.5]];

export const ICONS = {
  /* ---------- Bedienung ---------- */
  search: { t: 'Suche', s: circle(10.5, 10.5, 6.5) + 'M16.2 16.2 21 21' },
  'chevron-down': { t: 'Aufklappen', s: 'M4.5 8.5 12 16l7.5-7.5' },
  'chevron-up': { t: 'Zuklappen', s: 'M4.5 15.5 12 8l7.5 7.5' },
  'chevron-right': { t: 'Weiter', s: 'M8.5 4.5 16 12l-7.5 7.5' },
  'chevron-left': { t: 'Zurück', s: 'M15.5 4.5 8 12l7.5 7.5' },
  'arrow-right': { t: 'Mehr erfahren', s: 'M3 12h16.5M13.5 6l6 6-6 6' },
  close: { t: 'Schließen', s: 'M5.5 5.5l13 13M18.5 5.5l-13 13' },
  menu: { t: 'Menü', s: 'M3 7h18M3 12h18M10 17h11' },
  plus: { t: 'Öffnen', s: 'M12 4v16M4 12h16' },
  minus: { t: 'Schließen (Akkordeon)', s: 'M4 12h16' },
  check: { t: 'Erledigt', s: 'M4 12.5l5 5L20 6.5' },
  caret: { t: 'Pfeil klein', f: 'M9 7v10l6.5-5Z' },
  expand: { t: 'Vollbild', s: 'M14 3.5h6.5V10M10 20.5H3.5V14M18.5 5.5l-5 5M5.5 18.5l5-5' },
  pause: { t: 'Pause', f: 'M7 5h3.25v14H7ZM13.75 5H17v14h-3.25Z' },
  play: { t: 'Abspielen', f: 'M7.5 4.5v15L19.5 12Z' },
  sliders: {
    t: 'Filter',
    s: 'M3 7h3.75M12.25 7H21M3 12h8.75M17.25 12H21M3 17h1.25M9.75 17H21',
    a: raute(9.5, 7, 1.75) + raute(14.5, 12, 1.75) + raute(7.5, 17, 1.75),
  },
  sort: { t: 'Sortieren', s: 'M7 3.5v16M3.5 16l3.5 3.5 3.5-3.5M13 6h8M13 11h6M13 16h4' },
  share: { t: 'Teilen', s: 'M12 15V3.5M7.5 8 12 3.5 16.5 8M8.5 11H5v9.5h14V11h-3.5' },
  heart: { t: 'Merken', s: 'M12 20.25 4.6 12.85a4.55 4.55 0 0 1 6.45-6.45l.95.95.95-.95a4.55 4.55 0 0 1 6.45 6.45Z' },
  bell: { t: 'Suchauftrag', s: 'M5.5 17.5V11a6.5 6.5 0 0 1 13 0v6.5M3.5 17.5h17M10 20.75h4', a: raute(19.5, 4.5, 2) },
  image: { t: 'Bilder', s: 'M3 4.5h18v15H3ZM6 17l4-4 3.5 3.5 2-2 2.5 2.5', a: raute(16, 8.5, 1.5) },

  /* ---------- Kontakt & Navigation ---------- */
  user: { t: 'Konto', s: circle(12, 7.5, 3.75) + 'M4.5 21v-1.25c0-3.25 3-5.75 7.5-5.75s7.5 2.5 7.5 5.75V21' },
  pin: { t: 'Standort', s: PIN, a: raute(12, 10.75, 2.25) },
  globe: { t: 'Region / Sprache', s: GLOBE },
  phone: { t: 'Telefon', s: PHONE },
  mail: { t: 'E-Mail', s: 'M3 5.5h18v13H3ZM5 7.75l7 5.25 7-5.25' },
  sparkle: { t: 'KI-Suche', s: 'M10 7l6 6-6 6-6-6Z', a: raute(18.5, 5.5, 2.5) },
  buildings: {
    t: 'Objektart',
    s: 'M4 21V4h7.5v17M6.75 7.5h2M6.75 10.5h2M6.75 13.5h2M6.75 16.5h2M13 12.25l3.75-3.75 3.75 3.75M14 13.75V21M19.5 13.75V21M2.5 21h19',
  },

  /* ---------- Exposé-Kennzahlen ---------- */
  rooms: { t: 'Zimmer', s: 'M3.5 3.5h17v17h-17ZM12 3.5V9M12 12.5v8M3.5 12h5' },
  area: { t: 'Wohnfläche', s: 'M3.5 3.5h17v17h-17ZM8 16l8-8M12 7.5h4.5V12M7.5 12v4.5H12' },
  plot: {
    t: 'Grundstück',
    s: PLOT.map(([x, y], i) => seg(x, y, ...PLOT[(i + 1) % 4], 2.5)).join(''),
    a: PLOT.map(([x, y]) => raute(x, y, 1.25)).join(''),
  },
  energy: { t: 'Energie', s: 'M13.5 2.5 5.5 13.5h6l-1 8 8-11h-6Z' },

  /* ---------- Leistungen & Inhalte ---------- */
  house: { t: 'Haus', s: 'M2.5 11.5 12 3.5l9.5 8M5.5 13v8.5h13V13M10 21.5v-5h4v5', a: raute(12, 9.25, 1.25) },
  apartment: { t: 'Wohnung', s: 'M6 21.5V5h12v16.5M7.5 2.75h9M3 21.5h18M9 8h2M13 8h2M9 11.5h2M13 11.5h2M9 15h2M13 15h2M10.5 21.5v-3h3v3' },
  multi: {
    t: 'Mehrfamilienhaus',
    s: 'M3 9.5l4-4 4 4M4 11v10.5M10 11v10.5M12.5 21.5V3.5h8v18M15 7h3M15 10.5h3M15 14h3M2 21.5h20',
    a: raute(7, 14.5, 1.25),
  },
  sale: { t: 'Verkauf', s: 'M5 21.5V2.5M3.5 5h16M8.5 5v2.5M16.5 5v2.5M7 9h12v8H7ZM2.5 21.5h5', a: raute(13, 13, 1.75) },
  key: { t: 'Vermietung / Schlüssel', s: 'M7 7.5l4.5 4.5L7 16.5 2.5 12ZM13 12h8.5M17.5 12v3M20.5 12v2.5', a: raute(7, 12, 1.25) },
  advisor: { t: 'Beratung', s: circle(12, 6, 3.25) + 'M5 21.5V16c0-3 2.5-5 7-5s7 2 7 5v5.5', a: raute(12, 14.5, 1.75) },
  people: {
    t: 'Team',
    s: circle(9, 7.5, 3) + 'M3 20.5v-1c0-3 2.5-5 6-5s6 2 6 5v1M14.5 4.75a3 3 0 1 1 0 5.5M17 14.75c2.5.5 4 2.25 4 4.75v1',
  },
  chart: { t: 'Bewertung / Markt', s: 'M3 20.5h18M5 20.5v-6h3v6M10.5 20.5V11h3v9.5M16 20.5V8h3v12.5', a: raute(17.5, 4.25, 1.5) },
  money: { t: 'Finanzierung', s: 'M2.5 6.5h19v11h-19ZM12 9l3 3-3 3-3-3ZM5.5 9.5v5M18.5 9.5v5' },
  document: { t: 'Unterlagen', s: 'M5.5 2.5h9l4 4v15h-13ZM8.5 11h7M8.5 14h7M8.5 17h4' },
  signature: { t: 'Vertrag / Abwicklung', s: 'M14.5 4l4 4-9 9H5.5v-4ZM12.25 6.25l4 4M3 21h18' },
  camera: { t: 'Vermarktung / Fotos', s: 'M3 7.5h4.5L9 5h6l1.5 2.5H21v12H3Z' + circle(12, 13.25, 3.75), a: raute(18.25, 10, 0.9) },
  megaphone: { t: 'Werbung', s: 'M3.5 9.5v5h3l8.5 4.5V5L6.5 9.5ZM6.5 14.5l1.5 5h2.5l-1.25-4.5M18.5 12h3M18 7.75l2.5-1.5M18 16.25l2.5 1.5' },
  academy: {
    t: 'Wissen / Ratgeber',
    s: 'M2.5 9 12 4.5 21.5 9 12 13.5ZM6.5 11.5v4.75c1.5 1.25 3.5 2 5.5 2s4-.75 5.5-2V11.5M21.5 9v5.5',
    a: raute(21.5, 16.5, 1.25),
  },
  tools: { t: 'Online-Rechner', s: 'M3 4.5h18v12H3ZM12 18v2.5M8.5 20.5h7M11 9h6M11 12h4', a: raute(7.75, 10.5, 1.5) },
  shield: { t: 'Sicherheit', s: 'M12 2.75 4.5 5.75v5.5c0 4.5 3.25 8 7.5 9.75 4.25-1.75 7.5-5.25 7.5-9.75v-5.5ZM8.5 12l2.5 2.5 4.5-5' },
  calendar: { t: 'Termin', s: 'M3.5 5.5h17v15h-17ZM3.5 9.5h17M8 3v4.5M16 3v4.5', a: raute(15.5, 15, 1.75) },
  award: { t: 'Auszeichnung', s: circle(12, 9, 5.75) + 'M8.75 15.25 7.5 21.5l4.5-2.25 4.5 2.25-1.25-6.25', a: raute(12, 9, 2) },
  star: { t: 'Bewertung', s: 'M12 3l2.6 5.6 6.15.75-4.5 4.2 1.15 6.05L12 16.6l-5.4 3 1.15-6.05-4.5-4.2 6.15-.75Z' },
  compass: { t: 'Orientierung', s: circle(12, 12, 9) + 'M10 12l2 5.5 2-5.5', a: 'M12 6.5 14 12h-4Z' },
  sun: {
    t: 'Lage / Boden',
    s: circle(12, 12, 4) + 'M12 2.5V5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.75 1.75M16.95 16.95l1.75 1.75M5.3 18.7l1.75-1.75M16.95 7.05l1.75-1.75',
  },
  hand: {
    t: 'Übergabe',
    s: 'M8 8.5 12 5l4 3.5M9 9.75v3h6v-3M2.5 14.5h3l4.25 2h4.25a1.25 1.25 0 0 1 0 2.5H10.5M14 19l5.25-2.5a1.25 1.25 0 0 1 1.25 2.2L14 22H2.5',
  },
  bulb: { t: 'Idee / Tipp', s: 'M12 2.5a6.25 6.25 0 0 0-3.75 11.25v1.75h7.5v-1.75A6.25 6.25 0 0 0 12 2.5ZM9 17.5h6M10 20.5h4', a: raute(12, 8.75, 1.5) },
  eye: { t: 'Besichtigung', s: 'M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z' + circle(12, 12, 3.75), a: raute(12, 12, 1.5) },

  /* ---------- Illustrationen (48er Raster) ---------- */
  'ill-house': {
    t: 'Einfamilienhaus',
    vb: [48, 48],
    s: 'M4 22 24 6l20 16M33 12.5V8h4v7.5M9 24.5V41h30V24.5M21 41v-9h6v9M13 28h5v5h-5ZM30 28h5v5h-5ZM2 41h44',
    a: raute(24, 16.5, 1.75),
  },
  'ill-townhouse': {
    t: 'Giebelhäuser (Prinzipalmarkt)',
    vb: [48, 48],
    s: 'M4 41V18l6-7 6 7v23M18 41V14h2v-3h2V8h4v3h2v3h2v27M32 41V18l6-7 6 7v23'
      + 'M6.5 41v-5a3.5 3.5 0 0 1 7 0v5M20.5 41v-5a3.5 3.5 0 0 1 7 0v5M34.5 41v-5a3.5 3.5 0 0 1 7 0v5'
      + 'M8.5 21v3.5M11.5 21v3.5M8.5 27v3.5M11.5 27v3.5M22.5 18v3.5M25.5 18v3.5M22.5 24.5v3.5M25.5 24.5v3.5M36.5 21v3.5M39.5 21v3.5M36.5 27v3.5M39.5 27v3.5M2 41h44',
    a: raute(10, 15.5, 1.25) + raute(24, 12, 1.25) + raute(38, 15.5, 1.25),
  },
  'ill-apartment': {
    t: 'Wohnanlage',
    vb: [48, 48],
    s: 'M12 41V8h24v33M14 5.5h20M8.5 16H12M8.5 24H12M8.5 32H12M36 16h3.5M36 24h3.5M36 32h3.5'
      + 'M16.5 12h4M27.5 12h4M16.5 20h4M27.5 20h4M16.5 28h4M27.5 28h4M21 41v-6h6v6M2 41h44',
    a: raute(30.5, 37.5, 1.25),
  },
  'ill-save-search': {
    t: 'Suche speichern',
    vb: [120, 100],
    s: 'M54 50 80 30l26 20M60 54v38h40V54M74 92V76h12v16M66 60h8v8h-8ZM86 60h8v8h-8Z'
      + 'M14 44h40v26H14ZM30 73v19M20 52h16M20 59h12M8 92h104',
    a: raute(45, 57, 4),
  },
} satisfies Record<string, IconDef>;

export type IconName = keyof typeof ICONS;
