// Objekte aus der Vermittlung von Oberholz Immobilien (Quelle: listings.json, extrahiert von der bisherigen Website).
import raw from './listings.json';

export type PropertyType = 'Haus' | 'Wohnung' | 'Grundstück' | 'Gewerbe';
export type Mode = 'kaufen' | 'mieten';

export type Property = {
  id: string;
  title: string;
  district: string;
  city: string;
  zip: string;
  region: string;
  type: PropertyType;
  mode: Mode;
  price: number | null;
  priceLabel: string;
  provision: string;
  rooms?: number;
  living?: number;
  plot?: number;
  investment: boolean;
  energyClass?: string;
  badges: string[];
  images: string[];
  imageTotal: number;
  sections: Record<string, string[]>;
  daysOnline: number;
};

type Raw = (typeof raw)[number];

const STATES = ['Nordrhein-Westfalen', 'Niedersachsen'];
const NIEDERSACHSEN = ['Hitzacker', 'Auetal'];
export const REGION_GROUPS: Record<string, string[]> = {
  münsterland: ['Münster', 'Steinfurt', 'Coesfeld', 'Rheine', 'Stadtlohn'],
  ruhrgebiet: ['Essen', 'Bochum', 'Duisburg', 'Bergkamen', 'Bottrop', 'Velbert'],
};

function parseLocation(r: Raw) {
  let city = r.city.trim();
  let district = r.district.trim();
  let region = 'Nordrhein-Westfalen';
  for (const s of STATES) if (city.endsWith(s)) { region = s; city = city.slice(0, -s.length).trim(); }
  if (NIEDERSACHSEN.some((n) => city.startsWith(n))) region = 'Niedersachsen';
  if (city.includes(',')) { [city, district] = city.split(',').map((x) => x.trim()); }
  city = city.replace(/\s*-\s*/g, '-');
  const m = city.match(/^(Bottrop) (.+)$/);
  if (m) { city = m[1]; district = m[2]; }
  return { city, district, region };
}

/** Abschnitte fürs Exposé: „Beschreibung“ → „Objektbeschreibung“, fremde Ansprechpartner-Angaben entfallen */
function cleanSections(sec: Record<string, string[]>) {
  const out: Record<string, string[]> = {};
  for (const [k, v] of Object.entries(sec)) {
    if (k === 'Ansprechpartner' || !v?.length) continue;
    out[k === 'Beschreibung' ? 'Objektbeschreibung' : k] = v;
  }
  return out;
}

function toProperty(r: Raw, i: number): Property {
  const { city, district, region } = parseLocation(r);
  const t = r.title;
  const type: PropertyType = /Grundstück/i.test(t) && !/Haus|Wohnung/i.test(r.type) ? 'Grundstück'
    : r.type === 'Wohnung' ? 'Wohnung' : 'Haus';
  const investment = /Kapitalanlage|Rendite|Mehrfamilienhaus|vermietet|Appartements|Dreiparteienhaus/i.test(t);
  const energy = r.type.startsWith('Energie') ? r.type.replace('Energie', '').trim() : undefined;
  const area = r.area ?? undefined;
  return {
    id: r.id, title: t.replace(/\s+!/g, '!'), city, district, zip: r.zip, region, type,
    mode: r.mode === 'Miete' ? 'mieten' : 'kaufen',
    price: r.price ?? null, priceLabel: r.priceLabel ? r.priceLabel.charAt(0) + r.priceLabel.slice(1).toLowerCase() : 'Kaufpreis',
    provision: r.provision, rooms: r.rooms ?? undefined,
    living: type === 'Grundstück' ? undefined : area, plot: type === 'Grundstück' ? area : undefined,
    investment, energyClass: energy,
    badges: [...(Number(r.id) >= 171000000 ? ['Neu'] : []), ...(investment ? ['Kapitalanlage'] : [])],
    images: r.images, imageTotal: r.imageTotal, sections: cleanSections(r.sections as unknown as Record<string, string[]>),
    daysOnline: i,
  };
}

// Reihenfolge „Neueste zuerst“: höhere Objekt-Nr. = jüngeres Inserat
export const properties: Property[] = (raw as Raw[]).filter((r) => r.images.length > 0)
  .sort((a, b) => Number(b.id) - Number(a.id)).map(toProperty);
/** ungefähre Koordinaten der Orte für die Kartenansicht der Suche */
export const CITY_COORDS: Record<string, [number, number]> = {
  Münster: [51.96, 7.63], Essen: [51.456, 7.012], Bochum: [51.481, 7.216], Duisburg: [51.434, 6.762], Düsseldorf: [51.227, 6.773],
  Coesfeld: [51.946, 7.168], Stadtlohn: [51.993, 6.917], Rheine: [52.28, 7.44], Steinfurt: [52.15, 7.34], Bergkamen: [51.616, 7.644],
  Velbert: [51.34, 7.043], Krefeld: [51.339, 6.586], Bottrop: [51.524, 6.929], 'Kamp-Lintfort': [51.503, 6.546],
  'Hitzacker (Elbe)': [53.152, 11.043], Auetal: [52.233, 9.233],
};

export const findProperty = (id: string) => properties.find((p) => p.id === id);

const eur = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 0 });
export const formatPrice = (p: Property) =>
  p.price === null ? 'Preis auf Anfrage' : `${eur.format(p.price)} €${p.mode === 'mieten' ? ' Kaltmiete' : ''}`;
export const formatArea = (n: number) => `~${n.toLocaleString('de-DE', { maximumFractionDigits: 1 })} m²`;

/** Attributzeile wie in der Referenz: „5 Zimmer · ~153,8 m² Wohnfläche“ */
export const attributes = (p: Property) => [
  p.rooms ? `${p.rooms.toLocaleString('de-DE')} Zimmer` : null,
  p.living ? `${formatArea(p.living)} Wohnfläche` : null,
  p.plot ? `${formatArea(p.plot)} Grundstücksfläche` : null,
  p.energyClass ? `Energieklasse ${p.energyClass}` : null,
].filter(Boolean) as string[];

/** Ortsfilter inkl. Regionen („Münsterland“, „Ruhrgebiet“) */
export function matchesPlace(p: Property, query: string) {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  const group = REGION_GROUPS[q];
  if (group) return group.includes(p.city);
  return [p.district, p.city, p.region, p.zip, p.id, `${p.city}-${p.district}`].some((s) => s.toLowerCase().includes(q));
}
