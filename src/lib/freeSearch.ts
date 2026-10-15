// „KI-Suche“: wandelt eine frei formulierte Wunschbeschreibung lokal in Suchfilter um (ohne externen Dienst).
// Erkannt werden Ort/Stadtteil/Region, Kauf/Miete, Objektart, Preis (inkl. Spannen), Zimmer, Fläche und Ausstattung.
import { properties, REGION_GROUPS } from '../data/properties';
import { ROUTES } from '../data/routes';

export const PLACES = Array.from(new Set([
  ...properties.map((p) => p.city),
  ...properties.filter((p) => p.district).map((p) => `${p.city}-${p.district}`),
  'Münsterland', 'Ruhrgebiet',
])).sort((a, b) => a.localeCompare(b, 'de'));

/** Ausstattungsmerkmale: Suchbegriff → Muster im Exposé-Text */
export const FEATURES: Record<string, RegExp> = {
  Balkon: /balkon|loggia/i,
  Garten: /garten/i,
  Terrasse: /terrasse/i,
  Garage: /garage|tiefgarage|carport|stellplatz/i,
  Keller: /keller/i,
  Aufzug: /aufzug|fahrstuhl|lift\b/i,
  Barrierefrei: /barrierefrei|barrierearm|ebenerdig|bodengleich/i,
  Einbauküche: /einbauküche|ebk\b/i,
  Bezugsfrei: /bezugsfrei|leerstehend|frei ab/i,
  Vermietet: /vermietet|mieteinnahmen|kaltmiete pro monat/i,
};

const ascii = (s: string) => s.toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss');
const num = (s: string) => Number(s.replace(/\./g, '').replace(',', '.'));
const money = (value: string, unit = '', rent = false) => {
  let v = num(value);
  if (/^(tsd|tausend|k|t)$/i.test(unit)) v *= 1000;
  else if (/^(mio|millionen?)$/i.test(unit)) v *= 1_000_000;
  else if (!rent && v < 10_000) v *= 1000; // „bis 400“ → 400.000 €
  return Math.round(v);
};

export type Wish = { params: URLSearchParams; mieten: boolean; recognized: string[] };

export function interpretWish(text: string): Wish {
  const t = ` ${text.toLowerCase()} `;
  const a = ascii(t);
  const params = new URLSearchParams();
  const recognized: string[] = [];
  const mieten = /\b(miete|mieten|zur miete|kaltmiete|warmmiete|mietwohnung)\b/.test(t);
  if (mieten) recognized.push('Miete');

  // Ort: Stadtteile und Städte aus dem Bestand, dazu Regionen
  const districts = properties.filter((p) => p.district).map((p) => ({ name: p.district, city: p.city }));
  const district = districts.find((d) => d.name.length > 3 && (t.includes(d.name.toLowerCase()) || a.includes(ascii(d.name))));
  const city = [...new Set(properties.map((p) => p.city)), ...Object.keys(REGION_GROUPS).map((r) => r[0].toUpperCase() + r.slice(1))]
    .sort((x, y) => y.length - x.length)
    .find((c) => t.includes(c.toLowerCase()) || a.includes(ascii(c)));
  if (district) { params.set('ort', district.name); recognized.push(`${district.city}-${district.name}`); }
  else if (city) { params.set('ort', city); recognized.push(city); }

  // Objektart
  if (/mehrfamilienhaus|zinshaus|kapitalanlage|rendite|anleger|investment|vermietete?s? (haus|objekt)/.test(t)) { params.set('anlage', '1'); recognized.push('Kapitalanlage'); }
  const typ = /\b(wohnung|etw|eigentumswohnung|apartment|appartement|maisonette|penthouse)/.test(t) ? 'Wohnung'
    : /\b(haus|häuser|reihenhaus|einfamilienhaus|doppelhaus|doppelhaushälfte|bungalow|villa|zweifamilienhaus)/.test(t) ? 'Haus'
      : /\b(grundstück|bauland|baugrundstück)/.test(t) ? 'Grundstück' : null;
  if (typ) { params.set('typ', typ); recognized.push(typ); }

  // Preis: „zwischen 200.000 und 300.000“, „200–300 tsd“, „bis 1,2 mio“, „unter 350k“, „ab 250.000“
  const range = t.match(/(?:zwischen|von)?\s*(\d[\d.,]*)\s*(tsd|tausend|k|mio|millionen?)?\s*(?:€|euro)?\s*(?:und|bis|-|–)\s*(\d[\d.,]*)\s*(tsd|tausend|k|mio|millionen?)?\s*(?:€|euro)/);
  const max = t.match(/(?:bis|max\.?|maximal|höchstens|unter|nicht mehr als)\s*(\d[\d.,]*)\s*(tsd|tausend|k|mio|millionen?)?/);
  const min = t.match(/(?:ab|mindestens|über)\s*(\d[\d.,]*)\s*(tsd|tausend|k|mio|millionen?)?\s*(?:€|euro)/);
  if (range) {
    const unit = range[4] ?? range[2] ?? '';
    params.set('preis_min', String(money(range[1], range[2] ?? unit, mieten)));
    params.set('preis_max', String(money(range[3], unit, mieten)));
  } else {
    if (max && !/zimmer|qm|m²|quadrat/.test(t.slice(t.indexOf(max[0]), t.indexOf(max[0]) + max[0].length + 8))) params.set('preis_max', String(money(max[1], max[2], mieten)));
    if (min) params.set('preis_min', String(money(min[1], min[2], mieten)));
  }
  if (params.has('preis_max') || params.has('preis_min')) {
    const f = (v: string | null) => (v ? `${Number(v).toLocaleString('de-DE')} €` : '');
    recognized.push(params.has('preis_min') && params.has('preis_max') ? `${f(params.get('preis_min'))} – ${f(params.get('preis_max'))}` : params.has('preis_max') ? `bis ${f(params.get('preis_max'))}` : `ab ${f(params.get('preis_min'))}`);
  }

  // Zimmer: „3 Zimmer“, „3-Zi“, „ab 4 Zimmern“, „3–4 Zimmer“
  const rooms = t.match(/(?:ab|mindestens|min\.?)?\s*(\d)(?:\s*(?:-|–|bis)\s*\d)?\s*-?\s*(?:zi\b|zi\.|zimmer)/);
  if (rooms) { params.set('zimmer', rooms[1]); recognized.push(`ab ${rooms[1]} Zimmer`); }

  // Fläche: „ab 80 qm“, „mindestens 100 m²“, „120 quadratmeter“
  const area = t.match(/(?:ab|mindestens|min\.?|über)?\s*(\d{2,4})\s*(?:qm|m²|m2|quadratmeter)/);
  if (area) { params.set('flaeche_min', area[1]); recognized.push(`ab ${area[1]} m²`); }

  // Ausstattung
  const features = Object.keys(FEATURES).filter((k) => FEATURES[k].test(t) && !(k === 'Vermietet' && params.has('anlage')));
  if (features.length) { params.set('merkmale', features.join(',')); recognized.push(...features); }

  return { params, mieten, recognized };
}

export function parseWish(text: string) {
  const w = interpretWish(text);
  if (text.trim()) w.params.set('ki', text.trim().slice(0, 140));
  const base = w.mieten ? ROUTES.mieten : ROUTES.kaufen;
  return { url: `${base}${w.params.size ? `?${w.params}` : ''}`, recognized: w.recognized };
}

/** Beispiele für die KI-Suche (Startseite) */
export const WISH_EXAMPLES = [
  '3-Zimmer-Wohnung in Münster mit Balkon',
  'Haus mit Garten im Ruhrgebiet bis 450.000 €',
  'Kapitalanlage in Bochum',
  'Barrierefreie Wohnung in Essen',
];
