// Unternehmen, Kontakt und Regionen – Inhalte der bisherigen Website.
import { Link, useParams } from 'react-router-dom';
import { faqs, homeFaq, page, textOf, type RichBlock } from '../../data/oberholz';
import { brand, officeBySlug, offices, photos, team, whatsappUrl } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { REGION_GROUPS } from '../../data/properties';
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
import { BTN_CALL, BTN_KONTAKT, PropertyStrip, ServiceGrid, TeaserBand, TOOL_TEASERS, short, splitIntro } from './shared';

const U = [{ label: 'Über uns', to: ROUTES.ueberUns }];

export function TeamSection() {
  return (
    <section className="wrap" id="team" style={{ scrollMarginTop: 140 }}>
      <SectionIntro variant="inline" line={false} eyebrow="Unser Team" title="Ihre Ansprechpartner bei Oberholz Immobilien" text="Makler, Gutachter und Berater – persönlich für Sie da in Münster, Essen und Bochum." />
      <ul className="rich__team">
        {team.map((m) => (
          <li key={m.name}><span className="rich__team-img"><img src={m.image} alt={m.name} loading="lazy" /></span><strong>{m.name}</strong><span>{m.role}</span></li>
        ))}
      </ul>
      <div className="srch__center"><a href={brand.phoneHref} className="btn btn--outline">{brand.phoneDisplay}</a></div>
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
      <Partners kinds={['kooperation', 'finanzierung', 'portale']} id="partner" />
      <TeaserBand items={[
        { eyebrow: 'Qualifikationen', title: 'Energieberater, Gutachter und Makler', text: 'Gebündelte Fachkompetenz unter einem Dach – was das für Sie bedeutet.', to: ROUTES.qualifikation, cta: 'Mehr erfahren', image: photos.beratung },
        { eyebrow: 'Qualitätsmanagement', title: 'Auf dem Weg zur ISO 9001', text: 'Dokumentierte Abläufe und externe Audits für verlässliche Ergebnisse.', to: ROUTES.iso, cta: 'Zum Stand der Zertifizierung', image: photos.buero },
      ]} />
      <div className="rich"><div className="rich__text"><FaqBlock title="Häufige Fragen" items={homeFaq} /></div></div>
      <Contact variant="page" />
    </>
  );
}

export function Qualifikation() {
  const b = page('ueber-uns-qualifikation').blocks;
  usePageMeta({ title: 'Qualifikationen: Energieberater, Gutachter & Makler', crumbs: [...U, { label: 'Qualifikationen' }], footer: 'accordion', description: textOf(b[1]) });
  return (
    <>
      <PageHero eyebrow="Qualifikationen" title={textOf(b[0])} text={textOf(b[1])} image={photos.advisorA} cutout rating buttons={[BTN_KONTAKT, BTN_CALL]} />
      <Rich blocks={b.slice(2)} />
      <Contact variant="page" />
    </>
  );
}

export function Iso() {
  const b = page('ueber-uns-iso-9001-zertifizierung').blocks;
  usePageMeta({ title: 'ISO 9001 Zertifizierung in Vorbereitung', crumbs: [...U, { label: 'ISO 9001' }], footer: 'accordion', description: textOf(b[1]) });
  return (
    <>
      <PageHero eyebrow="Qualitätsmanagement" title={textOf(b[0])} text={textOf(b[1])} image={photos.buero} alt="Heller Besprechungsraum mit Eichentisch" buttons={[BTN_KONTAKT]} />
      <Rich blocks={b.slice(2)} />
      <Contact variant="page" />
    </>
  );
}

/* ---------- Kontakt ---------- */

function OfficeCards() {
  return (
    <div className="offices-grid">
      {offices.map((o) => (
        <article key={o.slug} className="office">
          <div className="office__img"><img src={o.image} alt={`Immobilie aus unserer Vermittlung in ${o.city}`} loading="lazy" /></div>
          <div className="office__body">
            <p className="eyebrow">Zuständig für</p>
            <h3 className="office__title head">{o.area}</h3>
            <p>Persönlich vor Ort in {o.city}</p>
            <div className="office__links">
              <Link to={ROUTES.region(o.slug)}><IconArrowRight size={16} />Immobilienmakler {o.city}</Link>
              <Link to={ROUTES.regionVerkaufen(o.slug)}><IconArrowRight size={16} />Immobilie verkaufen in {o.city}</Link>
              <Link to={ROUTES.kontaktStadt(o.slug)}><IconArrowRight size={16} />Kontakt {o.city}</Link>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}

function ContactInfo() {
  return (
    <aside className="info-card">
      <p className="head">{brand.name}</p>
      <p>{brand.street}<br />{brand.city.replace(', Deutschland', '')}</p>
      <p style={{ marginTop: 12 }}>Telefon: <a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a><br />WhatsApp: <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer" className="link-underline">Chat starten</a><br />Fax: {brand.fax}<br />E-Mail: <a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a></p>
      <p style={{ marginTop: 12 }}><strong>Öffnungszeiten</strong><br />{brand.hours}</p>
      <p style={{ marginTop: 12 }}><a href={brand.googleUrl} target="_blank" rel="noopener noreferrer" className="link-underline">Route in Google Maps öffnen</a></p>
    </aside>
  );
}

export function Kontakt() {
  usePageMeta({ title: 'Kontakt', crumbs: [{ label: 'Kontakt' }], footer: 'accordion', description: `Kontakt zu Oberholz Immobilien: ${brand.street}, ${brand.city.replace(', Deutschland', '')}, Telefon ${brand.phoneDisplay}. Persönliche Beratung zu Verkauf, Vermietung und Bewertung in Münster, Essen und Bochum.` });
  const b = page('kontakt-kontakt-aufnehmen').blocks;
  const paras = b.filter((x) => x.t === 'p').map(textOf);
  return (
    <>
      <PageHero eyebrow="Kontakt" title={textOf(b[0])} text={paras[0]} image={photos.advisorA} alt="Michael Oberholz" cutout rating buttons={[BTN_CALL]} />
      <section className="wrap" id="formular">
        <div className="contact-grid">
          <div>
            <SectionIntro variant="inline" line={false} eyebrow="Schreiben Sie uns" title={textOf(b[2])} text={`${paras[1]} ${paras[2]}`} />
            <ContactForm subject="Kontaktanfrage über die Website" submitLabel="Nachricht senden" />
          </div>
          <ContactInfo />
        </div>
      </section>
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Regionen" title={textOf(b.find((x) => x.t === 'h2' && /Standorte/.test(textOf(x))))} />
        <OfficeCards />
      </section>
      <Contact variant="page" />
    </>
  );
}

/** Stadtseiten „Ihr Immobilienmakler für …“ (bisher /kontakt/immobilienmakler-<stadt>) */
export function KontaktStadt() {
  const { city = '' } = useParams();
  const o = officeBySlug(city);
  usePageMeta(o ? { title: `Immobilienmakler ${o.city} – Kontakt`, crumbs: [{ label: 'Kontakt', to: ROUTES.kontakt }, { label: o.city }], footer: 'accordion', description: `Ihr Immobilienmakler für ${o.city}: Oberholz Immobilien begleitet Verkauf, Vermietung und Bewertung persönlich vor Ort – zuständig für ${o.area}.`, image: o.image, jsonLd: [localServiceLd(o.city, o.area, ROUTES.kontaktStadt(o.slug))] } : { title: 'Seite nicht gefunden' });
  if (!o) return <NotFound />;
  const b = page(`kontakt-immobilienmakler-${o.slug}`).blocks;
  const checks = (b[1] as { items: string[] }).items.map((x) => x.split(' - ')[0]);
  const from = b.findIndex((x) => x.t === 'p' && x.text === 'BESUCHEN SIE UNS');
  const to = b.findIndex((x, i) => i > from && x.t === 'img');
  const body: RichBlock[] = [...b.slice(2, from).filter((x) => !(x.t === 'p' && /^Weitere Informationen/.test(x.text))), ...b.slice(to + 1)];
  return (
    <>
      <PageHero eyebrow={`Immobilienmakler ${o.city}`} title={textOf(b[0])} checks={checks} image={photos.advisorA} cutout rating
        buttons={[{ label: 'Anfrage stellen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <section className="wrap"><div className="contact-grid"><div><SectionIntro variant="inline" line={false} eyebrow="Besuchen Sie uns" title="So finden Sie uns" text={`Zuständig für ${o.area}. Termine vor Ort nach Vereinbarung.`} /></div><ContactInfo /></div></section>
      <Rich blocks={body} />
      <Funnel title={`Immobilie in ${o.city} verkaufen oder vermieten?`} />
      <CityProperties city={o.city} slug={o.slug} />
      <Contact variant="page" />
    </>
  );
}

/* ---------- Regionen ---------- */

export function Regionen() {
  usePageMeta({ title: 'Regionen: Bochum, Essen, Münster', crumbs: [{ label: 'Regionen' }], footer: 'accordion', description: 'Oberholz Immobilien ist in Münster, Essen und Bochum aktiv – mit festen Ansprechpartnern für Verkauf, Vermietung und Wertermittlung im Münsterland und im Ruhrgebiet.' });
  const b = page('regionen').blocks;
  return (
    <>
      <PageHero eyebrow="Regionen" title={textOf(b[0])} text={`${textOf(b[1])} Persönliche Beratung, Verkauf und Wertermittlung – mit festen Ansprechpartnern vor Ort.`} image="/assets/stock/staedte/muensterland.jpg" alt="Landschaft im Münsterland" rating buttons={[BTN_KONTAKT, BTN_CALL]} />
      <section className="wrap"><OfficeCards /></section>
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Immobilien in der Umgebung" title="Auch im Umland für Sie da" />
        <div className="svc-grid svc-grid--3">
          {Object.entries(REGION_GROUPS).map(([k, cities]) => (
            <Link key={k} to={`${ROUTES.kaufen}?ort=${encodeURIComponent(k === 'münsterland' ? 'Münsterland' : 'Ruhrgebiet')}`} className="svc">
              <LineIcon name="pin" size={40} />
              <h3 className="svc__title head">{k === 'münsterland' ? 'Münsterland' : 'Ruhrgebiet'}</h3>
              <p className="svc__text">{cities.join(', ')}</p>
              <span className="svc__more">Immobilien ansehen <IconArrowRight size={18} /></span>
            </Link>
          ))}
          <Link to={ROUTES.kaufen} className="svc">
            <LineIcon name="globe" size={40} /><h3 className="svc__title head">Weitere Orte in NRW</h3>
            <p className="svc__text">Düsseldorf, Krefeld, Kamp-Lintfort und weitere Angebote aus unserer Vermittlung.</p>
            <span className="svc__more">Alle Immobilien <IconArrowRight size={18} /></span>
          </Link>
        </div>
      </section>
      <Contact variant="page" />
    </>
  );
}

function CityProperties({ city, slug }: { city: string; slug: string }) {
  const group = slug === 'muenster' ? REGION_GROUPS['münsterland'] : REGION_GROUPS['ruhrgebiet'];
  return (
    <PropertyStrip title={`Aktuelle Immobilien in ${city} und Umgebung`} filter={(p) => p.city === city || group.includes(p.city)}
      cta={{ label: `Alle Immobilien in ${city}`, to: `${ROUTES.kaufen}?ort=${encodeURIComponent(city)}` }} />
  );
}

function RegionPage({ kind }: { kind: 'makler' | 'verkaufen' }) {
  const { city = '' } = useParams();
  const o = officeBySlug(city);
  const key = o ? `regionen-${o.slug}-${kind === 'makler' ? 'immobilienmakler' : 'immobilie-verkaufen'}` : '';
  const label = o ? (kind === 'makler' ? `Immobilienmakler ${o.city}` : `Immobilie verkaufen in ${o.city}`) : '';
  usePageMeta(o ? { title: label, crumbs: [{ label: 'Regionen', to: ROUTES.regionen }, ...(kind === 'verkaufen' ? [{ label: o.city, to: ROUTES.region(o.slug) }] : []), { label: kind === 'makler' ? o.city : 'Immobilie verkaufen' }], footer: 'accordion', description: kind === 'makler' ? `Immobilienmakler für ${o.city}: Bewertung, Verkauf und Vermietung mit persönlichem Ansprechpartner vor Ort – Oberholz Immobilien, zuständig für ${o.area}.` : `Immobilie verkaufen in ${o.city}: realistische Wertermittlung, vollständige Unterlagen und professionelle Vermarktung mit Oberholz Immobilien.`, image: o.image, jsonLd: [localServiceLd(o.city, o.area, kind === 'makler' ? ROUTES.region(o.slug) : ROUTES.regionVerkaufen(o.slug), kind), faqLd(faqs(key))] } : { title: 'Seite nicht gefunden' });
  if (!o) return <NotFound />;
  const { title, checks, rest } = splitIntro(page(key).blocks);
  const advisor = rest.find((x) => x.t === 'img' && / - /.test(x.alt)) as { src: string } | undefined;
  const body = rest.filter((x) => x !== advisor);
  return (
    <>
      <PageHero eyebrow={o.area} title={title} checks={checks?.map(short)} image={advisor?.src ?? photos.advisorA} cutout rating
        buttons={[{ label: kind === 'makler' ? 'Kostenlose Erstberatung' : 'Immobilie bewerten lassen', to: '#anfrage', variant: 'accent' }, BTN_CALL]} />
      <Rich blocks={body} faq={faqs(key)} />
      <Funnel title={kind === 'makler' ? `Ihr Anliegen in ${o.city}` : `Immobilie in ${o.city} verkaufen`} intent={kind === 'verkaufen' ? 'Verkaufen' : undefined} />
      <CityProperties city={o.city} slug={o.slug} />
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow="Mehr zu Ihrer Region" title={`Rund um Immobilien in ${o.city}`} />
        <div className="svc-grid svc-grid--3">
          {kind === 'makler'
            ? <Link to={ROUTES.regionVerkaufen(o.slug)} className="svc"><LineIcon name="handshake" size={40} /><h3 className="svc__title head">Immobilie verkaufen in {o.city}</h3><span className="svc__more">Mehr erfahren <IconArrowRight size={18} /></span></Link>
            : <Link to={ROUTES.region(o.slug)} className="svc"><LineIcon name="advisor" size={40} /><h3 className="svc__title head">Immobilienmakler {o.city}</h3><span className="svc__more">Mehr erfahren <IconArrowRight size={18} /></span></Link>}
          <Link to={ROUTES.kontaktStadt(o.slug)} className="svc"><LineIcon name="pin" size={40} /><h3 className="svc__title head">Kontakt {o.city}</h3><span className="svc__more">So finden Sie uns <IconArrowRight size={18} /></span></Link>
          <Link to={ROUTES.bewertung} className="svc"><LineIcon name="chart" size={40} /><h3 className="svc__title head">Kostenlose Bewertung</h3><span className="svc__more">Wert ermitteln <IconArrowRight size={18} /></span></Link>
        </div>
      </section>
      <TeaserBand items={[TOOL_TEASERS.wertHebel, TOOL_TEASERS.immotipp]} />
      <ServiceGrid title="Unsere Leistungen" />
      <Contact variant="page" />
    </>
  );
}

export const Region = () => <RegionPage kind="makler" />;
export const RegionVerkaufen = () => <RegionPage kind="verkaufen" />;
