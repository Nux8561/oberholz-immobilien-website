import { Link, useParams } from 'react-router-dom';
import { officeBySlug, photos } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { ownerContent, ownerMarketSource, type OwnerCity, type OwnerKind } from '../../data/ownerContent';
import { faqLd, localServiceLd, usePageMeta } from '../../layout/PageMeta';
import PageHero from '../../components/PageHero/PageHero';
import Rich, { FaqBlock } from '../../components/Rich/Rich';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import ContactForm from '../../components/ContactForm/ContactForm';
import Contact from '../../components/Contact/Contact';
import { IconArrowRight } from '../../components/Icons';
import NotFound from '../NotFound';
import { BTN_CALL } from './shared';

export function OwnerLinks({ city, exclude }: { city?: OwnerCity; exclude?: OwnerKind }) {
  const cities: OwnerCity[] = city ? [city] : ['essen', 'bochum'];
  return <section className="wrap">
    <SectionIntro variant="inline" line={false} eyebrow="Für Eigentümer" title={city ? `Ihr nächster Schritt in ${officeBySlug(city)!.city}` : 'Verkauf und Bewertung in Essen und Bochum'} />
    <div className={`owner-links${city ? ' owner-links--local' : ''}`}>
      {cities.map((slug) => {
        const name = officeBySlug(slug)!.city;
        const links = [
          { kind: 'makler', label: `Immobilienmakler ${name}`, text: 'Persönliche Begleitung für Ihr Vorhaben.', to: ROUTES.region(slug), icon: 'advisor' },
          { kind: 'verkaufen', label: `Haus verkaufen in ${name}`, text: 'Von der Bewertung bis zur Übergabe.', to: ROUTES.regionVerkaufen(slug), icon: 'sale' },
          { kind: 'bewertung', label: `Immobilienbewertung ${name}`, text: 'Marktwert von Haus oder Wohnung einordnen.', to: ROUTES.regionBewertung(slug), icon: 'chart' },
          { kind: 'wohnung', label: `Wohnung verkaufen in ${name}`, text: 'Wohnung, Gemeinschaft und Vermietung berücksichtigen.', to: ROUTES.regionWohnungVerkaufen(slug), icon: 'apartment' },
        ].filter((x) => x.kind !== exclude);
        return <nav className="owner-links__group" key={slug} aria-label={`Weitere Eigentümerthemen ${name}`}>
          {!city && <h3 className="head">{name}</h3>}
          <ul>{links.map((x) => <li key={x.to}><Link to={x.to}><span>{x.label}</span><IconArrowRight size={18} /></Link></li>)}</ul>
        </nav>;
      })}
    </div>
  </section>;
}

export function OwnerGuides() {
  const guides = [
    ['immobilienwert-ermitteln', 'Wie viel ist mein Haus wert?', 'Bewertungsverfahren und wichtige Einflussfaktoren.'],
    ['immobilie-geerbt-der-erben-kompass-fuer-die-ersten-wochen', 'Geerbtes Haus: Was ist zuerst zu klären?', 'Nutzung, Unterlagen und die nächsten Entscheidungen.'],
    ['erst-sanieren-dann-verkaufen-was-sich-wirklich-rechnet', 'Haus verkaufen oder vorher sanieren?', 'Kosten, Zeitbedarf und mögliche Vorteile abwägen.'],
    ['maklerprovision-wer-zahlt', 'Was kostet ein Makler beim Hausverkauf?', 'Provision und Vereinbarungen verständlich erklärt.'],
    ['immobilie-bei-scheidung', 'Gemeinsame Immobilie bei Trennung', 'Verkauf, Übernahme oder Vermietung einordnen.'],
    ['haus-zu-gross-wie-der-wechsel-in-die-altersgerechte-wohnung-gelingt', 'Wenn das Haus im Alter zu groß wird', 'Wohnwechsel und die bisherige Immobilie gemeinsam planen.'],
  ];
  return <section className="wrap">
    <SectionIntro variant="inline" line={false} eyebrow="Fragen vor dem Verkauf" title="Erst Klarheit gewinnen, dann entscheiden" />
    <div className="svc-grid svc-grid--3">{guides.slice(0, 3).map(([slug, title, text]) => <Link key={slug} to={ROUTES.artikel(slug)} className="svc">
      <h3 className="svc__title head">{title}</h3><p className="svc__text">{text}</p>
      <span className="svc__more">Zum Ratgeber <IconArrowRight size={18} /></span>
    </Link>)}</div>
  </section>;
}

export function OwnerMarketSource({ city, tenancy = false }: { city: OwnerCity; tenancy?: boolean }) {
  const source = ownerMarketSource(city);
  return <aside className="owner-sources" aria-label="Quellen zur Markteinordnung">
    <p className="eyebrow">Quellen zur Markteinordnung</p>
    <ul>
      <li><a className="link-underline" href={source.href} target="_blank" rel="noopener noreferrer">{source.title}</a></li>
      <li><a className="link-underline" href="https://www.boris.nrw.de/boris-nrw/" target="_blank" rel="noopener noreferrer">BORIS-NRW: amtliche Informationen zum Grundstücksmarkt</a></li>
      {tenancy && <li><a className="link-underline" href="https://www.gesetze-im-internet.de/bgb/__566.html" target="_blank" rel="noopener noreferrer">§ 566 BGB: bestehendes Mietverhältnis beim Verkauf</a></li>}
    </ul>
  </aside>;
}

function LocalOwnerPage({ kind }: { kind: 'bewertung' | 'wohnung' }) {
  const { city = '' } = useParams();
  const o = officeBySlug(city);
  const slug = city as OwnerCity;
  const content = o ? ownerContent(slug, kind) : undefined;
  const isValuation = kind === 'bewertung';
  const path = isValuation ? ROUTES.regionBewertung(city) : ROUTES.regionWohnungVerkaufen(city);
  usePageMeta(content && o ? {
    title: content.metaTitle, description: content.description, image: photos.bewertung,
    footer: 'accordion',
    crumbs: [{ label: 'Standorte', to: ROUTES.regionen }, { label: o.city, to: ROUTES.region(city) }, { label: isValuation ? 'Immobilienbewertung' : 'Wohnung verkaufen' }],
    jsonLd: [localServiceLd(o.city, o.area, path, kind), faqLd(content.faq)],
  } : { title: 'Seite nicht gefunden', noindex: true });
  if (!o || !content) return <NotFound />;
  const topic = isValuation ? 'Immobilienbewertung' : 'Wohnungsverkauf';
  return <>
    <PageHero eyebrow={`${topic} · ${o.city}`} title={content.title} text={content.intro} checks={content.checks}
      image={isValuation ? photos.bewertung : o.image} alt={isValuation ? 'Persönliches Gespräch zur Immobilienbewertung' : `Blick auf ${o.city}`}
      buttons={[{ label: isValuation ? 'Bewertung anfragen' : 'Verkauf besprechen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
    <Rich blocks={content.blocks} />
    <section className="wrap" id="anfrage">
      <div className="lead">
        <SectionIntro variant="inline" line={false} eyebrow="Persönliches Erstgespräch"
          title={isValuation ? `Ihre Immobilie in ${o.city} einschätzen lassen` : `Ihre Wohnung in ${o.city} verkaufen`}
          text="Nennen Sie uns die Adresse, die Objektart und Ihr Anliegen. Wir besprechen mit Ihnen, welche Angaben und Unterlagen für den nächsten Schritt hilfreich sind." />
        <div className="lead__box"><ContactForm key={`${city}-${kind}`} subject={`${topic} ${o.city}`}
          submitLabel="Anfrage vorbereiten" message={`Ich möchte ${isValuation ? 'eine Immobilie bewerten lassen' : 'meine Eigentumswohnung verkaufen'} in ${o.city}. Adresse / Stadtteil: …\nAktuelle Nutzung und mein Anliegen: …`} /></div>
      </div>
    </section>
    <div className="rich"><div className="rich__text"><FaqBlock title={`Häufige Fragen zum Thema ${topic} in ${o.city}`} items={content.faq} /></div></div>
    <OwnerLinks city={slug} exclude={kind} />
    <OwnerGuides />
    <OwnerMarketSource city={slug} tenancy={!isValuation} />
    <Contact variant="page" />
  </>;
}

export const RegionBewertung = () => <LocalOwnerPage kind="bewertung" />;
export const RegionWohnungVerkaufen = () => <LocalOwnerPage kind="wohnung" />;
