import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { brand } from '../data/content';
import { SITE_URL } from '../data/routes';

export type Crumb = { label: string; to?: string };
export type PageMeta = {
  title?: string;
  crumbs?: Crumb[];
  footer?: 'open' | 'accordion';
  /** Meta-Description für Suchmaschinen (ca. 120–160 Zeichen) */
  description?: string;
  /** Vorschaubild für soziale Netzwerke (Pfad relativ zur Website) */
  image?: string;
  /** zusätzliche strukturierte Daten (schema.org, JSON-LD) */
  jsonLd?: object[];
  noindex?: boolean;
};

const DEFAULT_DESCRIPTION = `${brand.name}: Ihr Immobilienmakler in Münster, Essen und Bochum – Verkauf, Vermietung, kostenlose Bewertung und Rückmietverkauf, persönlich vor Ort.`;
const DEFAULT_IMAGE = '/assets/szenen/beratung.jpg';

const Ctx = createContext<{ meta: PageMeta; set: (m: PageMeta) => void }>({ meta: {}, set: () => {} });

export function PageMetaProvider({ children }: { children: ReactNode }) {
  const [meta, set] = useState<PageMeta>({});
  return <Ctx.Provider value={{ meta, set }}>{children}</Ctx.Provider>;
}
export const usePageMetaValue = () => useContext(Ctx).meta;

function setMeta(attr: 'name' | 'property', key: string, value: string) {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  if (!el) { el = document.createElement('meta'); el.setAttribute(attr, key); document.head.appendChild(el); }
  el.content = value;
}
function setLink(rel: string, href: string) {
  let el = document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`);
  if (!el) { el = document.createElement('link'); el.rel = rel; document.head.appendChild(el); }
  el.href = href;
}

const abs = (path: string) => (path.startsWith('http') ? path : `${SITE_URL}${path}`);

/** Seiten melden Titel, Breadcrumb, Footer-Variante und SEO-Angaben an das Layout. */
export function usePageMeta(meta: PageMeta) {
  const { set } = useContext(Ctx);
  const key = JSON.stringify(meta);
  useEffect(() => {
    set(meta);
    const title = meta.title ? `${meta.title} | ${brand.name}` : `${brand.name} | Immobilienmakler in Münster, Essen & Bochum`;
    const description = (meta.description ?? DEFAULT_DESCRIPTION).replace(/\s+/g, ' ').slice(0, 300);
    const url = `${SITE_URL}${window.location.pathname}`;
    document.title = title;
    setMeta('name', 'description', description);
    setMeta('name', 'robots', meta.noindex ? 'noindex, follow' : 'index, follow');
    setMeta('property', 'og:type', 'website');
    setMeta('property', 'og:site_name', brand.name);
    setMeta('property', 'og:locale', 'de_DE');
    setMeta('property', 'og:title', title);
    setMeta('property', 'og:description', description);
    setMeta('property', 'og:url', url);
    setMeta('property', 'og:image', abs(meta.image ?? DEFAULT_IMAGE));
    setMeta('name', 'twitter:card', 'summary_large_image');
    setLink('canonical', url);

    // Seitenbezogene strukturierte Daten: Breadcrumb + übergebene Daten
    const graph: object[] = [...(meta.jsonLd ?? [])];
    if (meta.crumbs?.length) {
      graph.push({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        itemListElement: [{ label: 'Startseite', to: '/' }, ...meta.crumbs].map((c, i) => ({
          '@type': 'ListItem', position: i + 1, name: c.label, ...(c.to ? { item: abs(c.to) } : {}),
        })),
      });
    }
    let script = document.getElementById('ld-page') as HTMLScriptElement | null;
    if (!script) { script = document.createElement('script'); script.type = 'application/ld+json'; script.id = 'ld-page'; document.head.appendChild(script); }
    script.textContent = graph.length ? JSON.stringify(graph) : '[]';
  }, [key]);
}

/* ---------- Bausteine für strukturierte Daten ---------- */

export const faqLd = (items: { q: string; a: string }[]) => ({
  '@context': 'https://schema.org', '@type': 'FAQPage',
  mainEntity: items.map((x) => ({ '@type': 'Question', name: x.q, acceptedAnswer: { '@type': 'Answer', text: x.a } })),
});

/** Stadtzentren der drei Kernregionen (für areaServed) */
const CITY_GEO: Record<string, [number, number]> = { Münster: [51.9607, 7.6261], Essen: [51.4556, 7.0116], Bochum: [51.4818, 7.2162] };
const LEISTUNGEN = ['Immobilienbewertung', 'Immobilienverkauf', 'Vermietung', 'Rückmietverkauf', 'Kapitalanlage', 'Finanzierungsvermittlung'];

/** Lokale Leistung „Immobilienmakler in <Stadt>“ – verknüpft mit der Organisation aus index.html (lokale Suche & KI-Antworten) */
export const localServiceLd = (city: string, area: string, path: string, kind: 'makler' | 'verkaufen' = 'makler') => {
  const geo = CITY_GEO[city];
  return {
    '@context': 'https://schema.org', '@type': 'Service',
    name: kind === 'makler' ? `Immobilienmakler ${city}` : `Immobilie verkaufen in ${city}`,
    serviceType: kind === 'makler' ? 'Immobilienmakler' : 'Immobilienverkauf',
    url: `${SITE_URL}${path}`,
    description: `${brand.name} begleitet Eigentümer, Käufer und Mieter in ${area}: kostenlose Bewertung, Verkauf, Vermietung und Rückmietverkauf mit persönlichem Ansprechpartner.`,
    provider: { '@id': `${SITE_URL}/#organisation` },
    areaServed: {
      '@type': 'City', name: city,
      ...(geo ? { geo: { '@type': 'GeoCoordinates', latitude: geo[0], longitude: geo[1] } } : {}),
      containedInPlace: { '@type': 'State', name: 'Nordrhein-Westfalen' },
    },
    hasOfferCatalog: {
      '@type': 'OfferCatalog', name: `Leistungen in ${city}`,
      itemListElement: LEISTUNGEN.map((n) => ({ '@type': 'Offer', itemOffered: { '@type': 'Service', name: `${n} ${city}` } })),
    },
  };
};
