// Objekte von Oberholz Immobilien (Quelle: listings.json, abgeglichen mit ImmoScout24 über scripts/import_immoscout.py).
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
  /** Ansprechpartner laut ImmoScout-Exposé („Angeboten von“) */
  agent: string;
  /** Telefon laut ImmoScout-Exposé, falls angegeben */
  agentPhone: string;
};

type Raw = (typeof raw)[number];

/** Regionen mit ihren Städten (Schlüssel = Ortsfilter in Kleinbuchstaben). Angezeigt werden nur Städte mit aktuellem Objekt.
 *  Zuordnung bewusst genau: Essen gehört zum Ruhrgebiet, Velbert und Wuppertal zum Bergischen Land, Düsseldorf zum Rheinland. */
export const REGION_GROUPS: Record<string, string[]> = {
  ruhrgebiet: ['Essen', 'Bochum', 'Duisburg', 'Gelsenkirchen', 'Mülheim an der Ruhr', 'Oberhausen', 'Bottrop', 'Gladbeck', 'Herne',
    'Dortmund', 'Hattingen', 'Witten', 'Bergkamen', 'Recklinghausen', 'Marl', 'Dorsten'],
  münsterland: ['Münster', 'Coesfeld', 'Stadtlohn', 'Steinfurt', 'Rheine', 'Greven', 'Borken', 'Dülmen', 'Warendorf', 'Telgte'],
  'bergisches land': ['Velbert', 'Wuppertal', 'Solingen', 'Remscheid', 'Heiligenhaus', 'Wülfrath'],
  rheinland: ['Düsseldorf', 'Ratingen', 'Neuss', 'Krefeld', 'Mönchengladbach', 'Köln'],
};
export const REGION_TITLES: Record<string, string> = {
  ruhrgebiet: 'Ruhrgebiet', münsterland: 'Münsterland', 'bergisches land': 'Bergisches Land', rheinland: 'Rheinland', weitere: 'Weitere Orte',
};
/** „Alle Immobilien im …“ */
export const REGION_IN: Record<string, string> = {
  ruhrgebiet: 'im Ruhrgebiet', münsterland: 'im Münsterland', 'bergisches land': 'im Bergischen Land', rheinland: 'im Rheinland',
};
export const regionOf = (city: string) =>
  Object.entries(REGION_GROUPS).find(([, cities]) => cities.includes(city))?.[0] ?? 'weitere';

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
  const t = r.title;
  const type: PropertyType = r.type === 'Wohnung' || r.type === 'Grundstück' ? r.type : 'Haus';
  const investment = /Kapitalanlage|Rendite|Mehrfamilienhaus|vermietet|Appartements|Dreiparteienhaus/i.test(t);
  const area = r.area ?? undefined;
  return {
    id: r.id, title: t.replace(/\s+!/g, '!'), city: r.city.trim(), district: r.district.trim(), zip: r.zip, region: 'Nordrhein-Westfalen', type,
    mode: r.mode === 'Miete' ? 'mieten' : 'kaufen',
    price: r.price ?? null, priceLabel: r.priceLabel ? r.priceLabel.charAt(0) + r.priceLabel.slice(1).toLowerCase() : 'Kaufpreis',
    provision: r.provision, rooms: r.rooms ?? undefined,
    living: type === 'Grundstück' ? undefined : area, plot: type === 'Grundstück' ? area : r.plot ?? undefined,
    investment, energyClass: r.energyClass || undefined,
    badges: [...(Number(r.id) >= 171000000 ? ['Neu'] : []), ...(investment ? ['Kapitalanlage'] : [])],
    images: r.images, imageTotal: r.imageTotal, sections: cleanSections(r.sections as unknown as Record<string, string[]>),
    daysOnline: i,
    agent: r.agent ?? '',
    agentPhone: r.agentPhone ?? '',
  };
}

// Reihenfolge „Neueste zuerst“: höhere Objekt-Nr. = jüngeres Inserat
export const properties: Property[] = (raw as Raw[]).filter((r) => r.images.length > 0)
  .sort((a, b) => Number(b.id) - Number(a.id)).map(toProperty);
/** ungefähre Koordinaten der Orte für die Kartenansicht der Suche */
export const CITY_COORDS: Record<string, [number, number]> = {
  Münster: [51.96, 7.63], Essen: [51.456, 7.012], Bochum: [51.481, 7.216], Duisburg: [51.434, 6.762], Düsseldorf: [51.227, 6.773],
  Coesfeld: [51.946, 7.168], Stadtlohn: [51.993, 6.917], Rheine: [52.28, 7.44], Steinfurt: [52.15, 7.34], Bergkamen: [51.616, 7.644],
  Velbert: [51.34, 7.043], Krefeld: [51.339, 6.586], Bottrop: [51.524, 6.929], Gelsenkirchen: [51.517, 7.085], Wuppertal: [51.256, 7.15],
};

export const findProperty = (id: string) => properties.find((p) => p.id === id);

const eur = new Intl.NumberFormat('de-DE', { maximumFractionDigits: 0 });
export const formatPrice = (p: Property) =>
  p.price === null ? 'Preis auf Anfrage' : `${eur.format(p.price)} €${p.mode === 'mieten' ? ' Kaltmiete' : ''}`;
export const formatArea = (n: number) => `~${n.toLocaleString('de-DE', { maximumFractionDigits: 1 })} m²`;

/** Attributzeile, z. B. „5 Zimmer · ~153,8 m² Wohnfläche“ */
export const attributes = (p: Property) => [
  p.rooms ? `${p.rooms.toLocaleString('de-DE')} Zimmer` : null,
  p.living ? `${formatArea(p.living)} Wohnfläche` : null,
  p.plot && !p.living ? `${formatArea(p.plot)} Grundstücksfläche` : null,
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
