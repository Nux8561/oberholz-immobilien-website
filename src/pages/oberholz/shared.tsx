// Gemeinsame Bausteine der Inhaltsseiten (Oberholz-Inhalte im Seiten-Template-Layout).
import { Link } from 'react-router-dom';
import { page, textOf, type QA, type RichBlock } from '../../data/oberholz';
import { brand, photos } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { properties, type Property } from '../../data/properties';
import type { Btn } from '../../blocks/Blocks';
import type { LineIconName } from '../../blocks/LineIcons';
import { LineIcon } from '../../blocks/LineIcons';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import PropertyCard from '../../components/PropertyCard/PropertyCard';
import { IconArrowRight, IconCheck } from '../../components/Icons';
import './pages.css';

/** Kopf einer übernommenen Seite: erste Überschrift, erster Absatz, erste Liste – der Rest geht an <Rich>. */
export function splitIntro(blocks: RichBlock[]) {
  const iH1 = blocks.findIndex((b) => b.t === 'h1' || b.t === 'h2');
  const title = textOf(blocks[iH1]);
  let i = iH1 + 1;
  let text: string | undefined;
  let checks: string[] | undefined;
  if (blocks[i]?.t === 'p') text = textOf(blocks[i++]);
  if (blocks[i]?.t === 'ul') checks = (blocks[i++] as { items: string[] }).items;
  const rest = [...blocks.slice(0, iH1).filter((b) => b.t === 'img'), ...blocks.slice(i)];
  return { title, text, checks, rest };
}

/** Kurzfassung für Listenpunkte „Titel: Erklärung“ (Hero-Häkchen) */
export const short = (s: string) => s.split(/:\s/)[0];

export const BTN_BEWERTUNG: Btn = { label: 'Kostenlose Bewertung', to: `${ROUTES.bewertung}#anfrage`, variant: 'accent' };
export const BTN_CALL: Btn = { label: `Anrufen: ${brand.phoneDisplay}`, to: brand.phoneHref, variant: 'outline', icon: 'phone' };
export const BTN_KONTAKT: Btn = { label: 'Kontakt aufnehmen', to: ROUTES.kontakt, variant: 'outline' };

export type Service = { key: string; title: string; text: string; to: string; icon: LineIconName; items: string[] };

const homeLists = page('home').blocks.filter((b) => b.t === 'ul').map((b) => (b as { items: string[] }).items);

/** Leistungsbereiche – Stichpunkte von der Startseite der bisherigen Website */
export const valuationMethods = homeLists[4];

export const services: Service[] = [
  { key: 'verkauf', title: 'Immobilie verkaufen', text: 'Vom realistischen Marktwert bis zum Notartermin – mit Konzept und Gutachterkompetenz.', to: ROUTES.verkaufen, icon: 'handshake', items: homeLists[1] },
  { key: 'bewertung', title: 'Immobilienbewertung', text: 'Kostenfreie, persönliche Einschätzung vor Ort – als Grundlage jeder Entscheidung.', to: ROUTES.bewertung, icon: 'chart', items: homeLists[2] },
  { key: 'vermietung', title: 'Vermietung', text: 'Marktgerechte Miete, geprüfte Mieter und ein rechtssicherer Mietvertrag.', to: ROUTES.vermieten, icon: 'key', items: homeLists[3] },
  { key: 'rueckmiet', title: 'Rückmietverkauf', text: 'Verkaufen und weiter im eigenen Zuhause wohnen.', to: ROUTES.rueckmietverkauf, icon: 'house', items: homeLists[5] },
  { key: 'finanzierung', title: 'Finanzierung', text: 'Bankengerechte Unterlagen und ein breites Banken-Netzwerk.', to: ROUTES.finanzierung, icon: 'money', items: ['Bankengerechte Unterlagen', 'Breites Banken-Netzwerk', 'Fördermittel- und KfW-Beratung'] },
  { key: 'vermarktung', title: 'Vermarktung', text: 'Exposés, Fotos, Visualisierungen – aus der eigenen Werbeagentur.', to: ROUTES.vermarktung, icon: 'camera', items: ['Hochwertige Exposés', 'Fotos, Videos & 3D-Visualisierungen', 'Reichweite auf führenden Portalen'] },
  { key: 'kapitalanlage', title: 'Kapitalanlage', text: 'Mehrfamilienhäuser und vermietete Wohnungen mit Ertragswertblick.', to: ROUTES.kapitalanlage, icon: 'multi', items: ['Mehrfamilienhäuser & Renditeobjekte', 'Ertragswert- und Mietanalyse', 'Finanzierung über unser Banken-Netzwerk'] },
  { key: 'abwicklung', title: 'Betreuung & Abwicklung', text: 'Verhandlung, Notar, Ämter – wir koordinieren alles bis zur Übergabe.', to: ROUTES.kontakt, icon: 'signature', items: homeLists[6] },
];

export function ServiceGrid({ exclude, title = 'Unsere Leistungen', eyebrow = 'Alles aus einer Hand' }: { exclude?: string; title?: string; eyebrow?: string }) {
  const list = services.filter((s) => s.key !== exclude);
  return (
    <section className="wrap">
      <SectionIntro variant="inline" line={false} eyebrow={eyebrow} title={title} />
      <div className="svc-grid">
        {list.map((s) => (
          <Link key={s.key} to={s.to} className="svc">
            <LineIcon name={s.icon} size={40} />
            <h3 className="svc__title head">{s.title}</h3>
            <p className="svc__text">{s.text}</p>
            {s.items.length > 0 && (
              <ul className="svc__list">{s.items.slice(0, 4).map((x) => <li key={x}><IconCheck size={14} />{x}</li>)}</ul>
            )}
            <span className="svc__more">Mehr erfahren <IconArrowRight size={18} /></span>
          </Link>
        ))}
      </div>
    </section>
  );
}

export function PropertyStrip({ title, eyebrow = 'Aktuelle Angebote', filter, cta }: { title: string; eyebrow?: string; filter: (p: Property) => boolean; cta: { label: string; to: string } }) {
  const list = properties.filter(filter).slice(0, 3);
  if (!list.length) return null;
  return (
    <section className="wrap">
      <SectionIntro variant="inline" line={false} eyebrow={eyebrow} title={title} />
      <div className="expo__similar-grid">{list.map((p) => <PropertyCard key={p.id} p={p} compact />)}</div>
      <div className="srch__center"><Link to={cta.to} className="btn btn--outline">{cta.label}</Link></div>
    </section>
  );
}

/** Teaser-Band zu Rechnern / Leitfäden */
export function TeaserBand({ items }: { items: { eyebrow: string; title: string; text: string; to: string; cta: string; image?: string }[] }) {
  const images = items.every((t) => t.image); // Bilder nur, wenn alle Kacheln eines haben (gleich hohe Reihe)
  return (
    <section className="wrap">
      <div className={`teasers teasers--${items.length}`}>
        {items.map((t) => (
          <Link key={t.title} to={t.to} className="teaser">
            {images && <span className="teaser__img"><img src={t.image} alt="" loading="lazy" /></span>}
            <span className="teaser__body">
              <span className="eyebrow">{t.eyebrow}</span>
              <span className="teaser__title head">{t.title}</span>
              <span className="teaser__text">{t.text}</span>
              <span className="teaser__cta">{t.cta} <IconArrowRight size={18} /></span>
            </span>
          </Link>
        ))}
      </div>
    </section>
  );
}

export const TOOL_TEASERS = {
  bewertung: { eyebrow: 'Immobilienbewertung', title: 'Was ist Ihre Immobilie wert?', text: 'Kostenlose und unverbindliche Einschätzung vor Ort – persönlich durch unser Team.', to: `${ROUTES.bewertung}#anfrage`, cta: 'Bewertung anfragen', image: '/assets/szenen/bewertung.jpg' },
  budget: { eyebrow: 'Budgetrechner', title: 'Kann ich mir eine Immobilie leisten?', text: 'Ihr realistischer Kaufpreisrahmen in zwei Minuten – ehrlich und ohne Anmeldung.', to: ROUTES.budgetrechner, cta: 'Budget prüfen', image: '/assets/ratgeber/kaufnebenkosten-nrw.jpg' },
  finanzierung: { eyebrow: 'Finanzierungsrechner', title: 'Nebenkosten, Rate und Restschuld', text: 'Mit Grunderwerbsteuer Ihres Bundeslandes und Zinsbindung nach Wahl.', to: ROUTES.finanzierungsrechner, cta: 'Rate berechnen', image: '/assets/szenen/beratung.jpg' },
  wertHebel: { eyebrow: 'Wert-Hebel-Rechner', title: 'Was bringt welche Modernisierung?', text: 'Überschlägig: Werteffekt, Kosten und Förderung einzelner Maßnahmen.', to: ROUTES.wertHebel, cta: 'Wert-Hebel prüfen', image: '/assets/ratgeber/energieausweis-beim-verkauf.jpg' },
  immotipp: { eyebrow: 'Immotipp', title: 'Tipp geben – ab 500 € Prämie', text: 'Sie kennen jemanden, der verkaufen möchte? Wir belohnen Ihren Hinweis.', to: ROUTES.immotipp, cta: 'Tipp abgeben', image: photos.schluessel },
};

export type FaqList = QA[];
