import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { attributes, findProperty, formatArea, formatPrice, properties, type Property } from '../../data/properties';
import { brand, photos, team, whatsappUrl } from '../../data/content';
import { ROUTES, SITE_URL } from '../../data/routes';
import { usePageMeta } from '../../layout/PageMeta';
import { useFavorites } from '../../lib/store';
import PropertyCard from '../../components/PropertyCard/PropertyCard';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import ContactForm from '../../components/ContactForm/ContactForm';
import Lightbox from '../../components/Lightbox/Lightbox';
import Deco from '../../components/Deco/Deco';
import FitImage from '../../components/FitImage/FitImage';
import { IconCheck, IconChevronRight, IconMail } from '../../components/Icons';
import { notify } from '../../components/Toast/Toast';
import NotFound from '../NotFound';
import './Expose.css';

const I = ({ d }: { d: string }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2" aria-hidden="true"><path d={d} /></svg>
);
const ICONS = {
  rooms: 'M4 20V5h10v15M14 9h6v11M3 20h18M10 12v2',
  area: 'M4 4h16v16H4zM4 9h5M15 4v5M9 20v-5M20 15h-5',
  plot: 'M3 20h18M5 20V9l7-5 7 5v11M3 16h18M9 20v-4h6v4',
  energy: 'M13 3 5 14h6l-1 7 8-11h-6Z',
  share: 'M12 15V3M8 7l4-4 4 4M5 11v9h14v-9',
  image: 'M3 5h18v14H3zM3 15l5-5 4 4 3-3 6 6M15 9h0',
};
const IconHeart = ({ on }: { on: boolean }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill={on ? 'var(--c-accent)' : 'none'} stroke={on ? 'var(--c-accent)' : 'currentColor'} strokeWidth="1.2" aria-hidden="true">
    <path d="M12 20.3 4.6 13a4.6 4.6 0 0 1 6.5-6.6l.9.9.9-.9A4.6 4.6 0 0 1 19.4 13Z" />
  </svg>
);

/** Exposé-Text: Zeilen mit „-“/„•“ werden zu Listen zusammengefasst. */
function SectionText({ lines }: { lines: string[] }) {
  const out: JSX.Element[] = [];
  let list: string[] = [];
  const flush = () => { if (list.length) { out.push(<ul key={out.length} className="expo__list">{list.map((l, i) => <li key={i}>{l}</li>)}</ul>); list = []; } };
  lines.forEach((l) => {
    const m = l.match(/^\s*[-•–]\s*(.+)$/);
    if (m) list.push(m[1]);
    else { flush(); out.push(<p key={out.length}>{l}</p>); }
  });
  flush();
  return <div className="expo__prose">{out}</div>;
}

const ORDER = ['Ausstattung', 'Lage', 'Sonstiges', 'Energieeffizienz'];

export default function Expose() {
  const { id = '' } = useParams();
  const p = findProperty(id);
  const favs = useFavorites();
  const [lb, setLb] = useState<number | null>(null);
  const [descOpen, setDescOpen] = useState(false);
  const agent = team[0];

  const similar = useMemo(() => (p ? properties.filter((x) => x.id !== p.id && x.mode === p.mode && (x.city === p.city || x.type === p.type)).slice(0, 3) : []), [p]);

  usePageMeta(p ? {
    title: p.title, footer: 'open', image: p.images[0],
    description: `${p.type} ${p.mode === 'mieten' ? 'zur Miete' : 'zum Kauf'} in ${p.zip} ${p.city}${p.district ? `-${p.district}` : ''}: ${p.title}. ${formatPrice(p)}${p.rooms ? `, ${p.rooms} Zimmer` : ''}${p.living ? `, ca. ${p.living} m² Wohnfläche` : ''}. Objekt-Nr. ${p.id}.`,
    jsonLd: [{
      '@context': 'https://schema.org', '@type': 'RealEstateListing',
      name: p.title, url: `${SITE_URL}${ROUTES.expose(p.id)}`, image: p.images.slice(0, 5).map((i) => `${SITE_URL}${i}`),
      description: (p.sections.Objektbeschreibung ?? []).slice(0, 2).join(' '),
      offers: p.price ? { '@type': 'Offer', price: p.price, priceCurrency: 'EUR', availability: 'https://schema.org/InStock', businessFunction: p.mode === 'mieten' ? 'http://purl.org/goodrelations/v1#LeaseOut' : 'http://purl.org/goodrelations/v1#Sell' } : undefined,
      about: { '@type': p.type === 'Wohnung' ? 'Apartment' : p.type === 'Grundstück' ? 'Place' : 'House', address: { '@type': 'PostalAddress', postalCode: p.zip, addressLocality: p.city, addressCountry: 'DE' }, ...(p.rooms ? { numberOfRooms: p.rooms } : {}), ...(p.living ? { floorSize: { '@type': 'QuantitativeValue', value: p.living, unitCode: 'MTK' } } : {}) },
      provider: { '@id': `${SITE_URL}/#organisation` },
    }],
  } : { title: 'Exposé nicht gefunden', noindex: true });
  if (!p) return <NotFound />;
  const fav = favs.has(p.id);

  const share = async () => {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title: p.title, url });
      else { await navigator.clipboard.writeText(url); notify('Link in die Zwischenablage kopiert.'); }
    } catch { notify('Teilen abgebrochen.'); }
  };
  const gallery = p.images.map((src, i) => ({ src, alt: `${p.title} – Bild ${i + 1}`, title: p.title }));
  const facts: [string, string][] = [
    ['Objekt-Nr.', p.id], ['Objektart', p.type], ['Vermarktung', p.mode === 'mieten' ? 'Miete' : 'Kauf'],
    ['Lage', `${p.zip} ${p.city}${p.district ? `, ${p.district}` : ''}`],
    ...(p.rooms ? [['Zimmer', p.rooms.toLocaleString('de-DE')] as [string, string]] : []),
    ...(p.living ? [['Wohnfläche', formatArea(p.living)] as [string, string]] : []),
    ...(p.plot ? [['Grundstücksfläche', formatArea(p.plot)] as [string, string]] : []),
    ...(p.energyClass ? [['Energieeffizienzklasse', p.energyClass] as [string, string]] : []),
    [p.priceLabel, formatPrice(p)],
    ...(p.provision ? [['Provision', p.provision.replace(/^zzgl\.\s*/, '')] as [string, string]] : []),
  ];
  const half = Math.ceil(facts.length / 2);
  const iconFacts = [
    p.rooms && [ICONS.rooms, `${p.rooms.toLocaleString('de-DE')} Zimmer`],
    p.living && [ICONS.area, `${formatArea(p.living)} Wohnfläche`], p.plot && [ICONS.plot, `${formatArea(p.plot)} Grundstücksfläche`],
    p.energyClass && [ICONS.energy, `Energieklasse ${p.energyClass}`],
  ].filter(Boolean) as [string, string][];
  const description = p.sections.Objektbeschreibung ?? [];
  const extra = ORDER.filter((k) => p.sections[k]?.length);
  const searchUrl = `${p.mode === 'mieten' ? ROUTES.mieten : ROUTES.kaufen}?ort=${encodeURIComponent(p.city)}`;

  return (
    <div className="expo">
      <div className="expo__actions">
        <button type="button" className="expo__action" onClick={share}><I d={ICONS.share} />Teilen</button>
        <button type="button" className="expo__action" aria-pressed={fav} onClick={() => notify(favs.toggle(p.id) ? 'Zur Merkliste hinzugefügt – zu finden unter „Mein Bereich“.' : 'Von der Merkliste entfernt.')}>
          <IconHeart on={fav} />{fav ? 'Auf der Merkliste' : 'Merken'}
        </button>
      </div>

      <div className="wrap expo__gallery-wrap">
        <div className="expo__gallery">
          {gallery.slice(0, 2).map((g, i) => (
            <button key={i} type="button" className="expo__img" onClick={() => setLb(i)} aria-label={`Bild ${i + 1} vergrößern`}>
              <FitImage src={g.src} alt={g.alt} eager />
            </button>
          ))}
          <button type="button" className="expo__count" onClick={() => setLb(0)} aria-label={`Alle ${gallery.length} Bilder anzeigen`}><I d={ICONS.image} />{gallery.length}</button>
        </div>
      </div>

      <div className="wrap expo__main">
        <div className="expo__info">
          <nav className="expo__crumbs" aria-label="Lage">
            <Link to={p.mode === 'mieten' ? ROUTES.mieten : ROUTES.kaufen} className="link-underline">Immobilien</Link><IconChevronRight size={20} />
            <Link to={searchUrl} className="link-underline">{p.city}</Link>
            {p.district && <><IconChevronRight size={20} /><span>{p.district}</span></>}
          </nav>
          <h1 className="expo__title head">{p.title}</h1>
          <div>
            <p className="expo__price head">{formatPrice(p)}</p>
            {p.provision && <p className="expo__prov">{p.provision}</p>}
          </div>
          {iconFacts.length > 0 && <ul className="expo__facts">{iconFacts.map(([d, t]) => <li key={t}><I d={d} />{t}</li>)}</ul>}
          {description.length > 0 && (
            <>
              <h2 className="expo__h2 head">Objektbeschreibung</h2>
              <div className={`expo__copy${descOpen ? ' is-open' : ''}`}><SectionText lines={description} /></div>
              {description.join(' ').length > 600 && <button type="button" className="link-underline expo__more" onClick={() => setDescOpen(!descOpen)}>{descOpen ? 'Weniger anzeigen' : 'Mehr anzeigen'}</button>}
            </>
          )}
        </div>
        <aside className="expo__agent">
          <img src={agent.face} alt={agent.name} className="expo__agent-img" />
          <h2 className="expo__agent-name head">{agent.name}</h2>
          <p className="expo__agent-meta">{agent.role}</p>
          <a href={brand.phoneHref} className="link-underline expo__agent-phone">{brand.phoneDisplay}</a>
          <a href="#anfrage" className="btn btn--accent btn--icon expo__agent-btn"><IconMail />Details anfragen</a>
          <a href={whatsappUrl(`Hallo Oberholz Immobilien, ich interessiere mich für das Objekt ${p.id} („${p.title}“). Bitte kontaktieren Sie mich.`)} target="_blank" rel="noopener noreferrer" className="link-underline expo__agent-wa">Per WhatsApp anfragen</a>
          <p className="expo__agent-meta">{brand.name}</p>
          <p className="expo__agent-meta">Objekt-Nr.: {p.id}</p>
        </aside>
      </div>

      <section className="expo__details">
        <div className="expo__inner">
          <h2 className="expo__h2 head">Objektdetails</h2>
          <div className="expo__table">
            {[facts.slice(0, half), facts.slice(half)].map((col, c) => (
              <dl key={c}>{col.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>
            ))}
          </div>
        </div>
      </section>

      {extra.map((k) => (
        <section key={k} className="expo__location">
          <div className="expo__inner">
            <h2 className="expo__h2 head">{k === 'Lage' ? `Lage: ${p.city}${p.district ? `-${p.district}` : ''}` : k}</h2>
            <div className="expo__text"><SectionText lines={p.sections[k]} /></div>
          </div>
        </section>
      ))}

      <section className="wrap expo__form-sec" id="anfrage">
        <span className="expo__line" aria-hidden="true" />
        <div className="expo__form-box">
          <SectionIntro variant="inline" line={false} center eyebrow="Fordern Sie alle Details zur Immobilie an" title="Mehr Informationen über diese Immobilie erhalten" />
          <ContactForm subject={`Exposé-Anfrage ${p.id}: ${p.title}`} message="Ich interessiere mich für diese Immobilie und hätte gerne weitere Informationen. Bitte kontaktieren Sie mich." />
        </div>
      </section>

      <div className="wrap">
        <article className="split expo__finance">
          <div className="split__media"><img src={photos.beratung} alt="Beratungsgespräch am Esstisch" loading="lazy" /></div>
          <div className="split__body">
            <p className="expo__brand"><strong>OBERHOLZ</strong> FINANZIERUNG</p>
            <h3 className="split__title head">Wunschimmobilie gefunden? Wir begleiten Ihre Finanzierung</h3>
            <ul className="expo__checks">
              {['Unverbindliche, kostenfreie Erstberatung', 'Banken-Netzwerk für finanzierungsstarke Lösungen', 'Fördermittel- und Energieberatung aus einem Haus'].map((t) => <li key={t}><span className="cform__tick"><IconCheck size={14} /></span>{t}</li>)}
            </ul>
            <div className="expo__fin-btns">
              <Link to={ROUTES.finanzierungsrechner} className="btn btn--outline split__cta">Rate berechnen</Link>
              <Link to={ROUTES.finanzierung} className="btn split__cta">Finanzierung anfragen</Link>
            </div>
          </div>
        </article>
      </div>

      {similar.length > 0 && (
        <section className="wrap expo__similar">
          <SectionIntro variant="inline" eyebrow="Weitere Angebote" title="Diese Immobilien könnten Sie ebenfalls interessieren" />
          <div className="expo__similar-grid">{similar.map((s: Property) => <PropertyCard key={s.id} p={s} compact />)}</div>
          <div className="srch__center"><Link to={searchUrl} className="btn btn--outline">Immobilien in {p.city}</Link></div>
        </section>
      )}

      <section className="expo__shop">
        <div className="wrap">
          <SectionIntro variant="inline" line={false} center eyebrow="Anbieter" title={brand.name} />
          <div className="expo__shop-row">
            <img src={photos.team} alt="Das Team von Oberholz Immobilien" className="expo__shop-img" />
            <div className="expo__shop-info">
              <p>{brand.company}</p>
              <p>Inhaber: {brand.owner}</p>
              <p><Link to={ROUTES.impressum} className="link-underline">Impressum</Link> • <Link to={ROUTES.datenschutz} className="link-underline">Datenschutz</Link></p>
              <p className="expo__shop-gap">{brand.street}, {brand.city.replace(', Deutschland', '')}</p>
              <p><a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a></p>
              <p><a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a></p>
            </div>
          </div>
          <div className="srch__center expo__shop-cta"><a href="#anfrage" className="btn btn--accent btn--icon btn--small"><IconMail />Details anfragen</a></div>
        </div>
      </section>

      <section className="expo__courtage">
        <div className="expo__courtage-inner">
          <h3 className="head">Provision</h3>
          <p>{p.provision
            ? `Für dieses Objekt fällt eine Käuferprovision von ${p.provision.replace(/^zzgl\.\s*/, '').replace(/\s*Käuferprovision/, '')} (laut Exposé) an.`
            : 'Die Konditionen zu diesem Objekt nennen wir Ihnen gerne persönlich und transparent vor einer Beauftragung.'}</p>
          <p className="expo__attrs">{attributes(p).join(' · ')}</p>
        </div>
      </section>
      <Deco />

      {lb !== null && <Lightbox images={gallery} index={lb} onIndex={setLb} onClose={() => setLb(null)} />}
    </div>
  );
}
