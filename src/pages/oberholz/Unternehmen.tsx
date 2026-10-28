// Unternehmen, Kontakt und Regionen – Inhalte der bisherigen Website.
import { Link, useParams } from 'react-router-dom';
import { homeFaq, page, textOf } from '../../data/oberholz';
import { brand, officeBySlug, officeLink, offices, photos, team, whatsappUrl } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { ownerContent, type OwnerCity } from '../../data/ownerContent';
import { OwnerGuides, OwnerLinks, OwnerMarketSource, SellSteps } from './LocalOwner';
import { properties, REGION_TITLES, regionOf } from '../../data/properties';
import { faqLd, localServiceLd, usePageMeta } from '../../layout/PageMeta';
import PageHero from '../../components/PageHero/PageHero';
import Rich, { FaqBlock } from '../../components/Rich/Rich';
import Funnel from '../../components/Funnel/Funnel';
import Contact from '../../components/Contact/Contact';
import ContactForm from '../../components/ContactForm/ContactForm';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import { IconArrowRight } from '../../components/Icons';
import { LineIcon } from '../../blocks/LineIcons';
import NotFound from '../NotFound';
import Partners from '../../components/Partners/Partners';
import { BTN_CALL, BTN_KONTAKT, PropertyStrip, callButton, splitIntro } from './shared';

/** Ansprechpartner im Kopf der Regionsseiten (Kunde Runde 3): Essen Felix Lesch, Münster Michael Oberholz */
const REGION_ADVISOR: Record<string, { image: string; name: string }> = {
  essen: { image: photos.advisorE, name: 'Felix Lesch' },
  muenster: { image: photos.advisorA, name: 'Michael Oberholz' },
};


export function TeamSection() {
  return (
    <section className="wrap" id="team" style={{ scrollMarginTop: 140 }}>
      <SectionIntro variant="inline" line={false} eyebrow="Unser Team" title="Ihre Ansprechpartner bei Oberholz Immobilien" text="Makler, Gutachter und Berater – persönlich für Sie da in Essen, Münster und Umgebung." />
      <ul className="rich__team">
        {team.map((m) => (
          <li key={m.name}>
            <span className="rich__team-img"><img src={m.image} alt={m.name} loading="lazy" /></span>
            <strong>{m.name}</strong>
            <span>{m.role}{m.office ? ` · ${m.office}` : ''}</span>
            {m.phoneDisplay && m.phoneHref ? (
              <a href={m.phoneHref} className="link-underline">{m.phoneDisplay}</a>
            ) : null}
          </li>
        ))}
      </ul>
      <div className="srch__center"><a href={brand.phoneHref} className="btn btn--outline">Zentrale {brand.phoneDisplay}</a></div>
    </section>
  );
}

export function UeberUns() {
  const { title, text, rest } = splitIntro(page('ueber-uns').blocks);
  usePageMeta({ title: 'Über uns: Team & Immobilienmakler Michael Oberholz', crumbs: [{ label: 'Über uns' }], footer: 'accordion', description: text, image: photos.team, jsonLd: [faqLd(homeFaq)] });
  return (
    <>
      <PageHero eyebrow="Über uns" title={title} text={text} image={photos.advisorG} alt="Michael Oberholz" cutout rating buttons={[BTN_KONTAKT, BTN_CALL]} />
      <Rich blocks={rest} />
      <TeamSection />
      <QualifikationSection />
      <Partners kinds={['kooperation', 'finanzierung', 'portale']} id="partner" />
      <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen" items={homeFaq} /></div></div>
      <Contact variant="page" />
    </>
  );
}

/** Qualifikationen und Qualitätsmanagement (früher eigene Unterseiten) als Abschnitt auf „Über uns“ */
function QualifikationSection() {
  const iso = page('ueber-uns-iso-9001-zertifizierung').blocks;
  return (
    <>
      <div id="qualifikation" style={{ scrollMarginTop: 140 }}>
        <Rich blocks={[
          { t: 'h2', text: 'Unsere Qualifikationen im Überblick' },
          { t: 'p', text: 'Oberholz Immobilien steht für gebündelte Fachkompetenz in Immobilienvermittlung und Wertermittlung – mit zugelassenen Maklern nach § 34c GewO und Gutachterkompetenz im Team.' },
          { t: 'h3', text: 'Immobilienmakler nach § 34c GewO' },
          { t: 'p', text: 'Wir vermitteln Immobilien mit der erforderlichen gewerberechtlichen Erlaubnis und begleiten Eigentümer sowie Kaufinteressenten persönlich durch den gesamten Prozess.' },
          { t: 'h3', text: 'Wertermittlung und Gutachterkompetenz' },
          { t: 'p', text: 'Marktwertermittlungen und gutachterliche Einschätzungen bilden die Grundlage für realistische Preise und nachvollziehbare Verkaufsstrategien.' },
          { t: 'h3', text: 'Vermarktung und Unterlagen' },
          { t: 'p', text: 'Exposé, Fotografie und die Abstimmung der erforderlichen Verkaufsunterlagen – einschließlich eines vorhandenen Energieausweises – gehören zu unserer Begleitung. Die Ausstellung von Energieausweisen gehört nicht zu unseren Leistungen.' },
        ]} />
      </div>
      <div id="qualitaet" style={{ scrollMarginTop: 140 }}><Rich blocks={[iso[0], iso[1], iso[6], iso[7]]} /></div>
    </>
  );
}

/* ---------- Kontakt ---------- */

function OfficeCards() {
  return (
    <div className="offices-grid">
      {offices.map((o) => (
        <article key={o.slug} className="office">
          <div className="office__img"><img src={o.image} alt={`Stadtansicht ${o.city}`} loading="lazy" /></div>
          <div className="office__body">
            <p className="eyebrow">Büro {o.city}</p>
            <h3 className="office__title head">{o.area}</h3>
            <p>{o.street}<br />{o.zipCity}<br />Telefon <a href={o.phoneHref} className="link-underline">{o.phoneDisplay}</a></p>
            <div className="office__links">
              <Link to={officeLink(o)}><IconArrowRight size={16} />Immobilienmakler {o.city}</Link>
              <Link to={ROUTES.regionVerkaufen(o.slug)}><IconArrowRight size={16} />Immobilie verkaufen in {o.city}</Link>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}

function ContactHubs() {
  const hubs = offices.filter((o) => o.hub);
  return (
    <aside className="info-card info-card--hubs">
      <p className="head">{brand.name}</p>
      <div className="info-card__hubs">
        {hubs.map((o) => {
          const person = team.find((m) => m.name === o.contactName);
          return (
            <div key={o.slug} className="info-card__hub">
              {person && <img src={person.face} alt={person.name} width={64} height={64} />}
              <p className="head" style={{ fontSize: 18 }}>{o.city}</p>
              {person && <p>{person.name}</p>}
              <p>{o.street}<br />{o.zipCity}</p>
              <p>Telefon: <a href={o.phoneHref} className="link-underline">{o.phoneDisplay}</a></p>
            </div>
          );
        })}
      </div>
      <p style={{ marginTop: 16 }}>WhatsApp: <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer" className="link-underline">{brand.whatsappDisplay}</a><br />E-Mail: <a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a></p>
      <p style={{ marginTop: 12 }}><strong>Öffnungszeiten</strong><br />{brand.hours}</p>
    </aside>
  );
}

export function Kontakt() {
  usePageMeta({ title: 'Kontakt', crumbs: [{ label: 'Kontakt' }], footer: 'accordion', description: `Kontakt zu Oberholz Immobilien in Essen (${brand.contactStreet}) und Münster (${brand.street}): Telefon Essen ${brand.phoneDisplay}, Münster ${brand.phoneMuensterDisplay}, WhatsApp ${brand.whatsappDisplay}.` });

  return (
    <>
      <PageHero eyebrow="Kontakt" title="Persönlich für Sie da" text="Sie planen einen Verkauf, suchen eine Immobilie oder haben Fragen zur Bewertung Ihrer Immobilie? Sprechen Sie mit unserem Team in Essen und Münster." image={photos.advisorE} alt="Felix Lesch" cutout rating buttons={[BTN_CALL]} />
      <section className="wrap" id="formular">
        <div className="contact-grid">
          <div>
            <SectionIntro variant="inline" line={false} eyebrow="Schreiben Sie uns" title="Wobei können wir Ihnen helfen?" text="Schildern Sie uns Ihr Anliegen. Wir besprechen mit Ihnen die nächsten Schritte." />
            <ContactForm subject="Kontaktanfrage über die Website" submitLabel="Nachricht senden" meta={{ form: 'kontaktseite', type: 'kontakt' }} />
          </div>
          <ContactHubs />
        </div>
      </section>
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Standorte" title="Unsere Büros in Essen und Münster" />
        <OfficeCards />
      </section>
    </>
  );
}

/* ---------- Regionen ---------- */

/** Regionen mit aktuellen Objekten, je Region die Orte in fester Reihenfolge von REGION_TITLES */
const listingRegions = () => Object.keys(REGION_TITLES)
  .map((k) => [k, [...new Set(properties.filter((p) => regionOf(p.city) === k).map((p) => p.city))]] as const)
  .filter(([, cities]) => cities.length > 0);

export function Regionen() {
  usePageMeta({ title: 'Standorte: Essen und Münster', crumbs: [{ label: 'Standorte' }], footer: 'accordion', description: 'Oberholz Immobilien mit Büros in Essen und Münster – feste Ansprechpartner für Verkauf, Vermietung und Wertermittlung im Ruhrgebiet, Rheinland, Bergischen Land und Münsterland.' });
  const b = page('regionen').blocks;
  return (
    <>
      <PageHero eyebrow="Standorte" title={textOf(b[0])} text={`${textOf(b[1])} Persönliche Beratung, Verkauf und Wertermittlung – mit festen Ansprechpartnern vor Ort.`} image="/assets/stock/staedte/muensterland.jpg" alt="Landschaft im Münsterland" rating buttons={[BTN_KONTAKT, BTN_CALL]} />
      <section className="wrap"><OfficeCards /></section>
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Immobilien in der Umgebung" title="Auch im Umland für Sie da" />
        <div className="svc-grid svc-grid--3">
          {/* nur Regionen und Orte mit aktuellem Objekt */}
          {listingRegions().map(([k, cities]) => (
            <Link key={k} to={k === 'weitere' ? ROUTES.kaufen : `${ROUTES.kaufen}?ort=${encodeURIComponent(REGION_TITLES[k])}`} className="svc">
              <LineIcon name={k === 'weitere' ? 'globe' : 'pin'} size={40} />
              <h3 className="svc__title head">{REGION_TITLES[k]}</h3>
              <p className="svc__text">{cities.join(', ')}</p>
              <span className="svc__more">Immobilien ansehen <IconArrowRight size={18} /></span>
            </Link>
          ))}
        </div>
      </section>
      <Contact variant="page" />
    </>
  );
}

function CityProperties({ city }: { city: string }) {
  return (
    <PropertyStrip title={`Aktuelle Immobilien in ${city}`} filter={(p) => p.city === city || p.city.startsWith(`${city}-`)}
      cta={{ label: `Alle Immobilien in ${city}`, to: `${ROUTES.kaufen}?ort=${encodeURIComponent(city)}` }} />
  );
}

function RegionPage({ kind }: { kind: 'makler' | 'verkaufen' }) {
  const { city = '' } = useParams();
  const o = officeBySlug(city);
  const content = o ? ownerContent(city as OwnerCity, kind) : undefined;
  const label = o ? (kind === 'makler' ? `Immobilienmakler ${o.city}` : `Immobilie verkaufen in ${o.city}`) : '';
  usePageMeta(o && content ? { title: content.metaTitle, crumbs: [{ label: 'Standorte', to: ROUTES.regionen }, ...(kind === 'verkaufen' ? [{ label: o.city, to: ROUTES.region(o.slug) }] : []), { label: kind === 'makler' ? o.city : 'Immobilie verkaufen' }], footer: 'accordion', description: content.description, image: o.image, jsonLd: [localServiceLd(o.city, o.area, kind === 'makler' ? ROUTES.region(o.slug) : ROUTES.regionVerkaufen(o.slug), kind), faqLd(content.faq)] } : { title: 'Seite nicht gefunden', noindex: true });
  if (!o || !content) return <NotFound />;
  const advisor = REGION_ADVISOR[o.slug] ?? REGION_ADVISOR.essen;
  return (
    <>
      <PageHero eyebrow={o.area} title={content.title} text={content.intro} checks={content.checks} image={advisor.image} alt={advisor.name} cutout rating
        buttons={[{ label: kind === 'makler' ? 'Kostenlose Erstberatung' : 'Immobilie bewerten lassen', to: '#anfrage', variant: 'accent' }, callButton(o)]} />
      <Rich blocks={content.blocks} />
      {content.stepsTitle && <SellSteps title={content.stepsTitle} />}
      {content.after && <Rich blocks={content.after} />}
      <div className="rich"><div className="rich__text"><FaqBlock title={`Häufige Fragen: ${label}`} items={content.faq} /></div></div>
      <Funnel title={kind === 'makler' ? `Ihr Anliegen in ${o.city}` : `Immobilie in ${o.city} verkaufen`} intent={kind === 'verkaufen' ? 'Verkaufen' : undefined} />
      <OwnerLinks city={city as OwnerCity} exclude={kind} />
      <OwnerGuides />
      <OwnerMarketSource city={city as OwnerCity} />
      {kind === 'makler' && <CityProperties city={o.city} />}
      <Contact variant="page" />
    </>
  );
}

export const Region = () => <RegionPage kind="makler" />;
export const RegionVerkaufen = () => <RegionPage kind="verkaufen" />;
