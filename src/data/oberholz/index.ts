// Zugriff auf die von der bisherigen Website übernommenen Inhalte (content.json, erzeugt von
// scripts/build_oberholz_content.py) plus abgeleitete Listen für Ratgeber, Whitepaper und Downloads.
import data from './content.json';
import type { EditorialArticle } from '../ratgeber/helpers';
import { kaeufer } from '../ratgeber/kaeufer';
import { verkaeufer } from '../ratgeber/verkaeufer';
import { eigentuemer } from '../ratgeber/eigentuemer';
import { AUTHOR_OF } from '../ratgeber/authors';
import { ARTICLE_IMAGE_ALT } from '../ratgeber/images';

export type RichBlock =
  | { t: 'h1' | 'h2' | 'h3' | 'h4' | 'p' | 'blockquote'; text: string }
  | { t: 'ul' | 'ol'; items: string[] }
  | { t: 'table'; rows: string[][] }
  | { t: 'img'; src: string; alt: string }
  | { t: 'pdf'; href: string; text: string };
export type RichPage = { title: string; blocks: RichBlock[] };
export type QA = { q: string; a: string };

const pages = data.pages as unknown as Record<string, RichPage>;
const faqMap = data.faqs as Record<string, QA[]>;

export function page(slug: string): RichPage {
  const p = pages[slug];
  if (!p) throw new Error(`Inhalt „${slug}“ fehlt in content.json`);
  return p;
}
/** echte FAQ-Einträge (ohne das als FAQ erfasste Inhaltsverzeichnis) */
export const faqs = (slug: string): QA[] => (faqMap[slug] ?? []).filter((f) => f.q !== 'Inhaltsverzeichnis');
export const homeFaq = data.homeFaq as QA[];

export const textOf = (b: RichBlock | undefined) => (b && 'text' in b ? b.text : '');
export const firstOf = (blocks: RichBlock[], t: RichBlock['t']) => blocks.find((b) => b.t === t);
export const itemsOf = (b: RichBlock | undefined) => (b && 'items' in b ? b.items : []);

/* ---------- Ratgeber ---------- */

export type Category = 'kaeufer' | 'verkaeufer' | 'eigentuemer';
export type Tool = 'budget' | 'finanzierung' | 'wertHebel' | 'bewertung';

export type Article = {
  slug: string; key: string; title: string; subtitle: string; intro: string;
  author: string; authorImage: string; date: string; image: string; thumb: string; imageAlt: string;
  toc: string[]; body: RichBlock[]; whitepaper?: string;
  category: Category; readingTime: number; facts: string[]; faq: QA[]; tools: Tool[];
};

/** Kategorien wie im E&V-Ratgeber (Käufer, Verkäufer, …) – zugeschnitten auf Oberholz */
export const CATEGORIES: { slug: Category; label: string; title: string; text: string }[] = [
  { slug: 'kaeufer', label: 'Käufer', title: 'Tipps für Käufer', text: 'Budget, Nebenkosten, Besichtigung und Kaufvertrag – so finden und finanzieren Sie die passende Immobilie.' },
  { slug: 'verkaeufer', label: 'Verkäufer', title: 'Tipps für Verkäufer', text: 'Bewertung, Unterlagen, Vermarktung und Steuern – so verkaufen Sie zum marktgerechten Preis.' },
  { slug: 'eigentuemer', label: 'Eigentümer & Erben', title: 'Tipps für Eigentümer, Vermieter und Erben', text: 'Vermieten, modernisieren, erben oder umziehen – Entscheidungshilfen rund um Ihre Immobilie.' },
];
export const categoryOf = (slug: string) => CATEGORIES.find((c) => c.slug === slug);

const ARTICLE_META: Record<string, { date: string; whitepaper: string; category: Category; tools: Tool[] }> = {
  'haus-zu-gross-wie-der-wechsel-in-die-altersgerechte-wohnung-gelingt': { date: '2026-08-26', whitepaper: 'wohnwechsel-im-alter', category: 'eigentuemer', tools: ['bewertung'] },
  'leerstand-vermietung-oder-verkauf-eine-ehrliche-abwaegung': { date: '2026-08-25', whitepaper: 'leerstand-vermietung-oder-verkauf', category: 'eigentuemer', tools: ['bewertung'] },
  'warum-ihre-unterlagen-ueber-die-finanzierung-ihrer-kaeufer-entscheiden': { date: '2026-08-25', whitepaper: 'unterlagen-und-finanzierung', category: 'verkaeufer', tools: ['finanzierung'] },
  'erst-sanieren-dann-verkaufen-was-sich-wirklich-rechnet': { date: '2026-08-25', whitepaper: 'sanieren-vor-dem-verkauf', category: 'verkaeufer', tools: ['wertHebel'] },
  'immobilie-geerbt-der-erben-kompass-fuer-die-ersten-wochen': { date: '2026-08-25', whitepaper: 'erben-kompass', category: 'eigentuemer', tools: ['bewertung'] },
  'der-grosse-generationenwechsel-was-der-silver-tsunami-fuer-immobilienverkaeufer-bedeutet': { date: '2026-08-25', whitepaper: 'generationenwechsel', category: 'verkaeufer', tools: ['bewertung'] },
};

const words = (blocks: RichBlock[]) => blocks.reduce((n, b) => n + ('text' in b ? b.text : 'items' in b ? b.items.join(' ') : 'rows' in b ? b.rows.flat().join(' ') : '').split(/\s+/).length, 0);
const minutes = (n: number) => Math.max(2, Math.round(n / 200));

function toArticle(slug: string): Article {
  const key = `ratgeber-${slug}`;
  const b = page(key).blocks;
  const author = b[2] as Extract<RichBlock, { t: 'img' }>;
  const header = b.find((x) => x.t === 'img' && x.src.includes('blog-article-header')) as Extract<RichBlock, { t: 'img' }>;
  const tocAt = b.findIndex((x) => x.t === 'h2' && x.text === 'Inhaltsverzeichnis');
  const end = b.findIndex((x) => x.t === 'ul' && x.items[0] === 'Teilen:');
  const toc = itemsOf(b[tocAt + 1]);
  const body = b.slice(tocAt + 2, end < 0 ? undefined : end)
    .filter((x) => !(x.t === 'p' && /^ZUM .*DOWNLOAD$|^WHITEPAPER .*$/.test(x.text)));
  return {
    slug, key, title: textOf(b[0]), subtitle: textOf(b[1]), intro: textOf(b[3]),
    author: author.alt, authorImage: author.src, date: ARTICLE_META[slug].date,
    image: `/assets/ratgeber/${slug}.jpg`, thumb: `/assets/ratgeber/${slug}.jpg`, imageAlt: ARTICLE_IMAGE_ALT[slug] ?? header.alt,
    toc, body, whitepaper: ARTICLE_META[slug].whitepaper,
    category: ARTICLE_META[slug].category, tools: ARTICLE_META[slug].tools,
    readingTime: minutes(words(body) + textOf(b[3]).split(/\s+/).length),
    facts: [], faq: [],
  };
}

const fromEditorial = (a: EditorialArticle): Article => ({
  slug: a.slug, key: `redaktion-${a.slug}`, title: a.title, subtitle: a.subtitle, intro: a.intro,
  author: AUTHOR_OF[a.slug] ?? 'Michael Oberholz', authorImage: '', date: a.date,
  image: `/assets/ratgeber/${a.slug}.jpg`, thumb: `/assets/ratgeber/${a.slug}.jpg`, imageAlt: ARTICLE_IMAGE_ALT[a.slug] ?? a.imageAlt,
  toc: a.body.filter((x) => x.t === 'h2').map(textOf), body: a.body, whitepaper: a.whitepaper,
  category: a.category, tools: a.tools ?? [], facts: a.facts, faq: a.faq,
  readingTime: minutes(words(a.body) + a.intro.split(/\s+/).length),
});

/** Alle Beiträge, neueste zuerst: Fachbeiträge der bisherigen Website + Redaktionsbeiträge */
export const articles: Article[] = [
  ...Object.keys(ARTICLE_META).map(toArticle),
  ...[...kaeufer, ...verkaeufer, ...eigentuemer].map(fromEditorial),
].sort((a, b) => b.date.localeCompare(a.date));
export const findArticle = (slug: string) => articles.find((a) => a.slug === slug);
export const formatDate = (iso: string) => new Date(`${iso}T12:00:00`).toLocaleDateString('de-DE', { day: '2-digit', month: 'long', year: 'numeric' });

/* ---------- Whitepaper / Leitfäden ---------- */

export type Whitepaper = { slug: string; title: string; intro: string; items: string[]; formTitle: string; image: string; facts: string; article?: Article };

const WP_KEYS: Record<string, string> = {
  generationenwechsel: 'whitepaper-generationenwechsel',
  'erben-kompass': 'erben-kompass',
  'sanieren-vor-dem-verkauf': 'whitepaper-sanieren-vor-dem-verkauf',
  'unterlagen-und-finanzierung': 'whitepaper-unterlagen-und-finanzierung',
  'leerstand-vermietung-oder-verkauf': 'whitepaper-leerstand-vermietung-oder-verkauf',
  'wohnwechsel-im-alter': 'whitepaper-wohnwechsel-im-alter',
};

/** Umfangsangaben aus „Leitfäden mit Anmeldung“ (Dokumente & Downloads) */
const WP_FACTS: Record<string, string> = {
  generationenwechsel: '13 Seiten, über 25 Quellen',
  'erben-kompass': '12 Seiten mit Checkliste zum Ausdrucken',
  'sanieren-vor-dem-verkauf': '9 Seiten mit Entscheidungsfahrplan',
  'unterlagen-und-finanzierung': '9 Seiten',
  'leerstand-vermietung-oder-verkauf': '10 Seiten',
  'wohnwechsel-im-alter': '9 Seiten',
};

export const whitepapers: Whitepaper[] = Object.entries(WP_KEYS).map(([slug, key]) => {
  const b = page(key).blocks;
  const article = articles.find((a) => a.whitepaper === slug && a.key.startsWith('ratgeber-')) ?? articles.find((a) => a.whitepaper === slug);
  return {
    slug, title: textOf(firstOf(b, 'h1')), intro: textOf(firstOf(b, 'p')), items: itemsOf(firstOf(b, 'ul')),
    formTitle: textOf(firstOf(b, 'h2')), image: article?.image ?? '', facts: WP_FACTS[slug], article,
  };
});
export const findWhitepaper = (slug: string) => whitepapers.find((w) => w.slug === slug);

/* ---------- Downloads ---------- */

export type Download = { href: string; title: string; text: string; size: string };
export type DownloadGroup = { title: string; items: Download[] };

const PDF_META: Record<string, [string, string]> = {
  objekt_erfassungsbogen: ['Objekt-Erfassungsbogen', '4,4 MB'],
  besichtigungsnachweis: ['Besichtigungsnachweis', '1,3 MB'],
  kaufabsichtserklaerung: ['Kaufabsichtserklärung', '1,3 MB'],
  makler_alleinvertrag: ['Makler-Alleinauftrag Verkauf', '1,3 MB'],
  makler_alleinauftrag_vermietung: ['Makler-Alleinauftrag Vermietung', '0,1 MB'],
  geschaeftsraummietvertrag: ['Geschäftsraummietvertrag', '0,7 MB'],
  merkblatt_ie: ['Merkblatt Immobilienvermittlung', '4,6 MB'],
  merkblatt_ea: ['Merkblatt Energieausweis', '0,5 MB'],
  merkblatt_wr: ['Merkblatt Sanierung & Förderung', '2,8 MB'],
  whitepaper_was_leisten_wir_fuer_sie: ['Whitepaper: Was leisten wir für Sie?', '0,4 MB'],
  'broschuere_energieberatung-oberholz': ['Broschüre: Vermittlung mit Energiekompetenz', '3,6 MB'],
};

/** Gruppen aus der Seite „Dokumente & Downloads“: Beschreibung (p) + PDF-Link paarweise */
export const downloadGroups: DownloadGroup[] = (() => {
  const b = page('dokumente-downloads').blocks;
  const groups: DownloadGroup[] = [];
  b.forEach((x, i) => {
    if (x.t === 'h2' && x.text !== 'Leitfäden mit Anmeldung') groups.push({ title: x.text, items: [] });
    if (x.t === 'pdf' && groups.length) {
      const name = x.href.split('/').pop()!.replace('.pdf', '');
      const [title, size] = PDF_META[name] ?? [name, ''];
      groups[groups.length - 1].items.push({ href: x.href, title, size, text: textOf(b[i - 1]) });
    }
  });
  return groups;
})();
export const downloadsIntro = textOf(page('dokumente-downloads').blocks[1]);
