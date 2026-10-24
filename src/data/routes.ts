// Alle Routen der Website an einer Stelle.

/** Produktiv-Domain (für Canonical, Sitemap, Open Graph) – vor dem Livegang prüfen */
export const SITE_URL = 'https://www.oberholz-immobilien.com';

export const ROUTES = {
  home: '/',
  kaufen: '/immobilien/kaufen',
  mieten: '/immobilien/mieten',
  expose: (id: string) => `/expose/${id}`,
  verkaufen: '/verkaufen',
  bewertung: '/bewertung',
  vermieten: '/vermieten',
  rueckmietverkauf: '/rueckmietverkauf',
  finanzierung: '/finanzierung',
  kapitalanlage: '/kapitalanlage',
  immotipp: '/immotipp',
  /** Rechner-Übersicht (im Ratgeber) */
  service: '/ratgeber#rechner',
  budgetrechner: '/service/budgetrechner',
  finanzierungsrechner: '/service/finanzierungsrechner',
  wertHebel: '/service/wert-hebel-rechner',
  ratgeber: '/ratgeber',
  artikel: (slug: string) => `/ratgeber/${slug}`,
  ratgeberThema: (slug: string) => `/ratgeber/thema/${slug}`,
  whitepaper: (slug: string) => `/whitepaper/${slug}`,
  /** Leitfäden & Downloads (im Ratgeber) */
  downloads: '/ratgeber#downloads',
  immopedia: '/immopedia',
  begriff: (slug: string) => `/immopedia/${slug}`,
  ueberUns: '/ueber-uns',
  team: '/ueber-uns#team',
  qualifikation: '/ueber-uns#qualifikation',
  kontakt: '/kontakt',
  regionen: '/regionen',
  region: (slug: string) => `/regionen/${slug}`,
  regionVerkaufen: (slug: string) => `/regionen/${slug}/verkaufen`,
  regionBewertung: (slug: string) => `/regionen/${slug}/immobilienbewertung`,
  regionWohnungVerkaufen: (slug: string) => `/regionen/${slug}/wohnung-verkaufen`,
  meinBereich: '/mein-bereich',
  impressum: '/impressum',
  datenschutz: '/datenschutz',
  cookieHinweise: '/cookie-hinweise',
} as const;

export const citySlug = (name: string) =>
  name.toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

/** Route für Linktexte aus Listen („Haus kaufen in Münster“ → gefilterte Suche) */
export function routeFor(label: string): string | null {
  const kauf = label.match(/^(Haus|Wohnung) kaufen (?:in|auf|am|an der|in den) (.+)$/);
  if (kauf) return `${ROUTES.kaufen}?ort=${encodeURIComponent(kauf[2])}&typ=${kauf[1]}`;
  return null;
}

/** Cloudflare Pages liefert die vorgerenderten Verzeichnisse mit abschließendem Slash. */
export const canonicalPageUrl = (path: string) => `${SITE_URL}${path.split(/[?#]/)[0].replace(/\/+$/, '')}/`;
