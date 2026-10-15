import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { CITY_COORDS, matchesPlace, properties, REGION_GROUPS, type Mode, type Property, type PropertyType } from '../../data/properties';
import { brand, offices } from '../../data/content';
import { articles } from '../../data/oberholz';
import { ROUTES } from '../../data/routes';
import { usePageMeta } from '../../layout/PageMeta';
import { useSavedSearches } from '../../lib/store';
import { FEATURES, interpretWish, parseWish } from '../../lib/freeSearch';
import PropertyCard from '../../components/PropertyCard/PropertyCard';
import Stars from '../../components/Stars/Stars';
import { openRatings } from '../../components/RatingPanel/RatingPanel';
import Accordion from '../../components/Accordion/Accordion';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import Contact from '../../components/Contact/Contact';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import { IconArrowRight, IconChevronDown, IconChevronLeft, IconChevronRight, IconClose, IconSearch } from '../../components/Icons';
import { notify } from '../../components/Toast/Toast';
import './Search.css';

const PER_PAGE = 35;
const TYPES: PropertyType[] = ['Haus', 'Wohnung', 'Grundstück'];
const SORTS = { neu: 'Neueste zuerst', preis_auf: 'Preis aufsteigend', preis_ab: 'Preis absteigend', flaeche: 'Größte Fläche' } as const;
type SortKey = keyof typeof SORTS;

const IconBell = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.25" aria-hidden="true">
    <path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 1.5h-15ZM10 20.5a2 2 0 0 0 4 0" /><path d="M18.5 4.5v3M17 6h3" />
  </svg>
);
const IconSliders = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.25" aria-hidden="true">
    <path d="M6 3v18M12 3v18M18 3v18" /><rect x="4" y="13" width="4" height="3" fill="#fff" /><rect x="10" y="6" width="4" height="3" fill="#fff" /><rect x="16" y="15" width="4" height="3" fill="#fff" />
  </svg>
);
const IconSort = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.25" aria-hidden="true">
    <path d="M7 4v16M4 17l3 3 3-3M13 6h8M13 11h6M13 16h4" />
  </svg>
);

/** Dropdown-Hülle der Filterleiste (schließt bei Klick außerhalb) */
function Pop({ label, active, children }: { label: string; active?: boolean; children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const f = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false); };
    document.addEventListener('mousedown', f); return () => document.removeEventListener('mousedown', f);
  }, []);
  return (
    <div className="fpop" ref={ref}>
      <button type="button" className={`fbtn${active ? ' is-active' : ''}`} aria-expanded={open} onClick={() => setOpen((o) => !o)}>
        <span>{label}</span><IconChevronDown size={20} />
      </button>
      {open && <div className="fpop__panel">{children}</div>}
    </div>
  );
}

const textCache = new Map<string, string>();
/** Volltext eines Exposés (Titel + alle Abschnitte) für die Merkmal-Suche */
const fullText = (p: Property) => {
  if (!textCache.has(p.id)) textCache.set(p.id, [p.title, ...Object.values(p.sections).flat()].join(' '));
  return textCache.get(p.id)!;
};

const regionOf = (city: string) =>
  Object.entries(REGION_GROUPS).find(([, cities]) => cities.includes(city))?.[0] ?? 'weitere';
const REGION_TITLES: Record<string, string> = { münsterland: 'Münsterland', ruhrgebiet: 'Ruhrgebiet', weitere: 'Weitere Orte' };

export default function Search() {
  const { mode: modeParam } = useParams();
  const mode: Mode = modeParam === 'mieten' ? 'mieten' : 'kaufen';
  const [qs, setQs] = useSearchParams();
  const navigate = useNavigate();
  const saved = useSavedSearches();

  const ort = qs.get('ort') ?? '';
  const typen = (qs.get('typ') ?? '').split(',').filter(Boolean) as PropertyType[];
  const anlage = qs.get('anlage') === '1';
  const pmin = Number(qs.get('preis_min') ?? '') || 0;
  const pmax = Number(qs.get('preis_max') ?? '') || 0;
  const zimmer = Number(qs.get('zimmer') ?? '') || 0;
  const flaecheMin = Number(qs.get('flaeche_min') ?? '') || 0;
  const merkmale = (qs.get('merkmale') ?? '').split(',').filter((m) => m in FEATURES);
  const ki = qs.get('ki') ?? '';
  const sort = (qs.get('sort') as SortKey) || 'neu';
  const page = Math.max(1, Number(qs.get('seite') ?? '1') || 1);
  const karte = qs.get('karte') === '1';

  const [ai, setAi] = useState(false);
  const [draft, setDraft] = useState(ort);
  const [moreOpen, setMoreOpen] = useState(false);
  useEffect(() => setDraft(ort), [ort]);

  const update = (patch: Record<string, string | null>) => {
    const next = new URLSearchParams(qs);
    Object.entries(patch).forEach(([k, v]) => (v ? next.set(k, v) : next.delete(k)));
    if (!('seite' in patch)) next.delete('seite');
    setQs(next);
  };

  const where = ort || 'NRW und Umgebung';
  const what = anlage ? 'Kapitalanlage' : typen.length === 1 ? typen[0] : 'Immobilie';
  const heading = `${what} ${mode === 'mieten' ? 'mieten' : 'kaufen'} in ${where}`;
  usePageMeta({ title: heading, footer: 'open', description: `${heading}: aktuelle Häuser, Wohnungen und Kapitalanlagen aus der Vermittlung von Oberholz Immobilien – mit persönlichem Ansprechpartner vor Ort.`, noindex: qs.toString().length > 0 && !(qs.size === 1 && qs.has('ort')) });

  const inMode = useMemo(() => properties.filter((p) => p.mode === mode), [mode]);
  const results = useMemo(() => {
    const list = inMode.filter((p) =>
      matchesPlace(p, ort) &&
      (!typen.length || typen.includes(p.type)) &&
      (!anlage || p.investment) &&
      (!pmin || (p.price ?? Infinity) >= pmin) &&
      (!pmax || (p.price !== null && p.price <= pmax)) &&
      (!zimmer || (p.rooms ?? 0) >= zimmer) &&
      (!flaecheMin || (p.living ?? p.plot ?? 0) >= flaecheMin) &&
      merkmale.every((m) => FEATURES[m].test(fullText(p))));
    const price = (p: Property) => p.price ?? Number.MAX_SAFE_INTEGER;
    return [...list].sort((a, b) =>
      sort === 'preis_auf' ? price(a) - price(b)
        : sort === 'preis_ab' ? (b.price ?? -1) - (a.price ?? -1)
          : sort === 'flaeche' ? (b.living ?? b.plot ?? 0) - (a.living ?? a.plot ?? 0)
            : a.daysOnline - b.daysOnline);
  }, [inMode, ort, typen.join(), anlage, pmin, pmax, zimmer, flaecheMin, merkmale.join(), sort]);

  // Orts-Chips mit echten Trefferzahlen
  const chips = useMemo(() => {
    const count = new Map<string, number>();
    inMode.forEach((p) => count.set(p.city, (count.get(p.city) ?? 0) + 1));
    return [...count.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'de'));
  }, [inMode]);

  const regions = useMemo(() => {
    const g = new Map<string, Map<string, number>>();
    properties.forEach((p) => {
      const r = regionOf(p.city);
      if (!g.has(r)) g.set(r, new Map());
      g.get(r)!.set(p.city, (g.get(r)!.get(p.city) ?? 0) + 1);
    });
    return ['münsterland', 'ruhrgebiet', 'weitere'].filter((r) => g.has(r)).map((r) => ({ key: r, cities: [...g.get(r)!.entries()] }));
  }, []);

  const pages = Math.max(1, Math.ceil(results.length / PER_PAGE));
  const shown = results.slice((page - 1) * PER_PAGE, page * PER_PAGE);
  const saveSearch = () => {
    const url = `${window.location.pathname}${window.location.search}`;
    notify(saved.add(heading, url) ? 'Suche gespeichert – Sie finden sie unter „Mein Bereich“.' : 'Diese Suche ist bereits gespeichert.');
  };

  const submitWhere = (e: React.FormEvent) => {
    e.preventDefault();
    if (ai) { navigate(parseWish(draft).url); return; }
    update({ ort: draft.trim() || null });
  };
  const toggleType = (t: PropertyType) => update({ typ: (typen.includes(t) ? typen.filter((x) => x !== t) : [...typen, t]).join(',') || null });

  return (
    <>
      <div className="srch">
        <div className="fbar">
          <form className="fbar__inner" onSubmit={submitWhere} role="search" aria-label="Suchfilter">
            <label className={`fbar__ai${ai ? ' is-on' : ''}`}>
              <span className="fbar__ai-label">KI-Suche</span>
              <input type="checkbox" className="sr-only" checked={ai} onChange={(e) => setAi(e.target.checked)} />
              <span className="switch" aria-hidden="true"><span /></span>
            </label>
            <label className="fsel">
              <span className="sr-only">Kaufen oder Mieten</span>
              <select value={mode} onChange={(e) => navigate(`${e.target.value === 'mieten' ? ROUTES.mieten : ROUTES.kaufen}${ort ? `?ort=${encodeURIComponent(ort)}` : ''}`)}>
                <option value="kaufen">Kaufen</option><option value="mieten">Mieten</option>
              </select>
              <IconChevronDown size={20} />
            </label>
            <div className="fbar__where">
              <IconSearch />
              <input value={draft} onChange={(e) => setDraft(e.target.value)} placeholder={ai ? 'z. B. Haus in Essen bis 450.000 €' : 'Stadt, Stadtteil, Postleitzahl oder Objekt-Nr.'} aria-label="Eingabe des Suchorts" />
              {draft && <button type="button" className="fbar__clear" aria-label="Ort löschen" onClick={() => { setDraft(''); update({ ort: null }); }}><IconClose size={18} /></button>}
            </div>
            <Pop label={anlage ? 'Kapitalanlage' : typen.length ? typen.join(', ') : 'Objektart'} active={typen.length > 0 || anlage}>
              {TYPES.map((t) => (
                <label key={t} className="fcheck"><input type="checkbox" checked={typen.includes(t)} onChange={() => toggleType(t)} />{t}</label>
              ))}
              <label className="fcheck"><input type="checkbox" checked={anlage} onChange={() => update({ anlage: anlage ? null : '1' })} />Kapitalanlage</label>
            </Pop>
            <Pop label={pmin || pmax ? `${pmin ? `${pmin.toLocaleString('de-DE')} €` : '0 €'} – ${pmax ? `${pmax.toLocaleString('de-DE')} €` : 'max'}` : 'Preis'} active={!!(pmin || pmax)}>
              <div className="frange">
                <label>Min.<input type="number" inputMode="numeric" min={0} step={10000} defaultValue={pmin || ''} placeholder="0 €" onBlur={(e) => update({ preis_min: e.target.value || null })} /></label>
                <label>Max.<input type="number" inputMode="numeric" min={0} step={10000} defaultValue={pmax || ''} placeholder="beliebig" onBlur={(e) => update({ preis_max: e.target.value || null })} /></label>
              </div>
            </Pop>
            <button type="button" className={`btn btn--outline btn--small fbar__more${zimmer || flaecheMin || merkmale.length ? ' is-active' : ''}`} onClick={() => setMoreOpen(true)}><IconSliders />Filter</button>
            <span className="fbar__sep" aria-hidden="true" />
            <button type="button" className="btn btn--accent btn--small btn--icon" onClick={saveSearch}><IconBell />Suche speichern</button>
            <button type="submit" className="sr-only">Suchen</button>
          </form>
        </div>

        {moreOpen && (
          <div className="fdrawer" role="dialog" aria-modal="true" aria-label="Weitere Filter">
            <div className="fdrawer__panel">
              <div className="fdrawer__head"><p className="head">Weitere Filter</p><button type="button" aria-label="Schließen" onClick={() => setMoreOpen(false)}><IconClose /></button></div>
              <p className="eyebrow">Zimmer (mindestens)</p>
              <div className="fdrawer__chips">
                {[0, 2, 3, 4, 5, 6].map((z) => <button key={z} type="button" className={`chip${zimmer === z ? ' is-active' : ''}`} onClick={() => update({ zimmer: z ? String(z) : null })}>{z ? `${z}+` : 'Alle'}</button>)}
              </div>
              <p className="eyebrow">Wohnfläche (mindestens)</p>
              <div className="fdrawer__chips">
                {[0, 60, 80, 100, 140].map((f) => <button key={f} type="button" className={`chip${flaecheMin === f ? ' is-active' : ''}`} onClick={() => update({ flaeche_min: f ? String(f) : null })}>{f ? `${f} m²` : 'Alle'}</button>)}
              </div>
              <p className="eyebrow">Ausstattung</p>
              <div className="fdrawer__chips">
                {Object.keys(FEATURES).map((m) => (
                  <button key={m} type="button" className={`chip${merkmale.includes(m) ? ' is-active' : ''}`}
                    onClick={() => update({ merkmale: (merkmale.includes(m) ? merkmale.filter((x) => x !== m) : [...merkmale, m]).join(',') || null })}>{m}</button>
                ))}
              </div>
              <button type="button" className="btn fdrawer__apply" onClick={() => setMoreOpen(false)}>{results.length} Ergebnisse anzeigen</button>
            </div>
            <button type="button" className="fdrawer__backdrop" aria-label="Schließen" onClick={() => setMoreOpen(false)} />
          </div>
        )}

        <div className="srch__container">
          <h1 className="srch__title head">{heading} – {results.length} {results.length === 1 ? 'Ergebnis' : 'Ergebnisse'}</h1>
          {ki && (
            <div className="kibox" role="status">
              <p className="kibox__q"><span className="kibox__badge">KI-Suche</span> „{ki}“</p>
              <ul className="kibox__chips">
                {interpretWish(ki).recognized.map((r) => <li key={r}>{r}</li>)}
                {interpretWish(ki).recognized.length === 0 && <li className="is-empty">Keine Kriterien erkannt – zeige alle Angebote</li>}
              </ul>
              <button type="button" className="link-underline" onClick={() => setQs(new URLSearchParams())}>KI-Filter zurücksetzen</button>
            </div>
          )}
          {merkmale.length > 0 && !ki && (
            <ul className="kibox__chips kibox__chips--plain">{merkmale.map((m) => <li key={m}>{m} <button type="button" aria-label={`${m} entfernen`} onClick={() => update({ merkmale: merkmale.filter((x) => x !== m).join(',') || null })}>×</button></li>)}</ul>
          )}
          <ul className="srch__chips">
            {chips.map(([c, n]) => (
              <li key={c}><button type="button" className="link-underline" onClick={() => update({ ort: c })}>{c} ({n})</button></li>
            ))}
          </ul>
          <div className="srch__toolbar">
            <label className="srch__sort">
              <IconSort />
              <select value={sort} onChange={(e) => update({ sort: e.target.value === 'neu' ? null : e.target.value })} aria-label="Sortieren">
                {Object.entries(SORTS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </label>
            <label className="srch__map">
              Karte
              <input type="checkbox" className="sr-only" checked={karte} onChange={(e) => update({ karte: e.target.checked ? '1' : null })} />
              <span className="switch" aria-hidden="true"><span /></span>
            </label>
          </div>

          {karte && <MapView items={shown} />}

          {shown.length === 0 ? (
            <div className="srch__empty">
              <p className="head">Aktuell keine passenden Angebote</p>
              <p>Viele Objekte vermitteln wir diskret, bevor sie veröffentlicht werden. Speichern Sie Ihre Suche oder sprechen Sie uns direkt an.</p>
              <div className="srch__empty-btns">
                <button type="button" className="btn btn--outline" onClick={() => setQs(new URLSearchParams())}>Filter zurücksetzen</button>
                <Link to={ROUTES.kontakt} className="btn">Suchauftrag besprechen</Link>
              </div>
            </div>
          ) : (
            <div className="srch__grid">
              {shown.map((p, i) => (
                <FragmentWithPromo key={p.id} index={i} onSave={saveSearch}><PropertyCard p={p} /></FragmentWithPromo>
              ))}
            </div>
          )}

          {pages > 1 && (
            <nav className="pager" aria-label="Seiten">
              <button type="button" disabled={page === 1} aria-label="Vorherige Seite" onClick={() => update({ seite: String(page - 1) })}><IconChevronLeft /></button>
              {Array.from({ length: pages }, (_, i) => i + 1).map((n) => (
                <button key={n} type="button" className={n === page ? 'is-active' : ''} aria-current={n === page ? 'page' : undefined} onClick={() => update({ seite: n === 1 ? null : String(n) })}>{n}</button>
              ))}
              <button type="button" disabled={page === pages} aria-label="Nächste Seite" onClick={() => update({ seite: String(page + 1) })}><IconChevronRight /></button>
            </nav>
          )}
          <p className="srch__disclaimer">
            Alle Angebote stammen aus der Vermittlung von {brand.name}. Angaben laut Eigentümer bzw. Exposé, ohne Gewähr. Zwischenverkauf und -vermietung vorbehalten.
          </p>
        </div>
      </div>

      <section className="wrap srch-sec">
        <SectionIntro variant="inline" line={false} eyebrow="Ratgeber" title={mode === 'mieten' ? 'Wissen rund um Ihre Immobilie' : 'Gut vorbereitet kaufen und verkaufen'} />
        <div className="guides">
          {articles.filter((a) => a.category === 'kaeufer').slice(0, 3).map((a) => (
            <Link key={a.slug} to={ROUTES.artikel(a.slug)} className="guide">
              <span className="guide__img"><img src={a.thumb} alt={a.imageAlt} loading="lazy" /></span>
              <h3 className="guide__title head">{a.title}</h3>
              <p className="guide__text">{a.subtitle}</p>
              <IconArrowRight className="guide__arrow" />
            </Link>
          ))}
        </div>
        <div className="srch__center"><Link to={ROUTES.ratgeber} className="btn btn--outline">Alle Beiträge</Link></div>
      </section>

      <section className="wrap srch-sec">
        <SectionIntro variant="inline" line={false} eyebrow="Persönlich vor Ort" title="Ihre Ansprechpartner in der Region" text="Ob Kauf, Verkauf oder Vermietung – unser Team ist in Münster, Essen und Bochum für Sie da." />
        <div className="offices">
          {offices.map((o) => (
            <Link key={o.slug} to={ROUTES.region(o.slug)} className="city b-tile">
              <div className="city__media"><img src={o.image} alt={`Immobilie aus unserer Vermittlung in ${o.city}`} loading="lazy" /></div>
              <div className="city__body"><h3 className="city__name head">Immobilienmakler {o.city}</h3><p className="city__sub">{o.area}</p></div>
              <span className="city__link"><IconArrowRight /></span>
            </Link>
          ))}
        </div>
        <div className="srch__center"><Link to={ROUTES.regionen} className="btn btn--outline">Alle Regionen</Link></div>
      </section>

      <section className="wrap srch-sec">
        <SectionIntro variant="inline" line={false} eyebrow="Orte" title="Alle Immobilien nach Region" />
        <Accordion variant="compact" columns={2} items={regions.map((r) => ({
          title: `${REGION_TITLES[r.key]} (${r.cities.reduce((s, [, n]) => s + n, 0)})`,
          content: (
            <ul className="region-links">
              {r.key !== 'weitere' && <li><Link to={`${ROUTES.kaufen}?ort=${encodeURIComponent(REGION_TITLES[r.key])}`}>Alle Immobilien im {REGION_TITLES[r.key]}</Link></li>}
              {r.cities.map(([c, n]) => <li key={c}><Link to={`${ROUTES.kaufen}?ort=${encodeURIComponent(c)}`}>Immobilien in {c} ({n})</Link></li>)}
            </ul>
          ),
        }))} />
      </section>

      <section className="wrap srch-sec srch-rating">
        <p className="eyebrow srch-rating__eyebrow">Bewertungen &amp; Rezensionen</p>
        <div className="rating">
          <p className="rating__title head">{brand.name}</p>
          <div className="rating__grid">
            <div><p className="head">{brand.rating.toFixed(1).replace('.', ',')}</p><Stars value={brand.rating} /></div>
            <div><p className="head">{brand.reviews}</p><p className="eyebrow">Google-Bewertungen</p></div>
            <div><p className="head">{offices.length}</p><p className="eyebrow">Regionen</p></div>
          </div>
          <p className="rating__note">Durchschnitt der Google-Bewertungen. <button type="button" className="link-underline" onClick={openRatings}>Bewertungen ansehen</button> · <a href={brand.googleUrl} target="_blank" rel="noopener noreferrer" className="link-underline">Google-Unternehmensprofil</a></p>
        </div>
      </section>

      <Breadcrumb items={[{ label: 'Immobilien', to: ROUTES.kaufen }, { label: mode === 'mieten' ? 'Mieten' : 'Kaufen' }]} />
      <Contact variant="page" />
    </>
  );
}

/** Kartenansicht ohne externen Kartendienst: ein Marker je Ort (Anzahl der Treffer), Klick filtert auf den Ort.
 *  Orte außerhalb des NRW-Ausschnitts werden darunter aufgeführt. */
function MapView({ items }: { items: Property[] }) {
  const byCity = new Map<string, Property[]>();
  items.forEach((p) => byCity.set(p.city, [...(byCity.get(p.city) ?? []), p]));
  const inNrw = (c: [number, number]) => c[0] < 52.6 && c[1] < 8.8;
  const pts = [...byCity.entries()].map(([city, list]) => ({ city, list, c: CITY_COORDS[city] })).filter((x) => x.c && inNrw(x.c));
  const outside = [...byCity.entries()].filter(([city]) => !CITY_COORDS[city] || !inNrw(CITY_COORDS[city]));
  const [la0, la1, lo0, lo1] = [51.15, 52.45, 6.3, 8.0];
  const pos = (c: [number, number]) => ({ left: `${((c[1] - lo0) / (lo1 - lo0)) * 100}%`, top: `${((la1 - c[0]) / (la1 - la0)) * 100}%` });
  const minPrice = (l: Property[]) => Math.min(...l.map((p) => p.price ?? Infinity));
  return (
    <div className="srch__mapwrap">
      <div className="srch__mapview" role="img" aria-label="Kartenansicht der Suchergebnisse nach Ort">
        <span className="srch__region" style={{ left: '62%', top: '18%' }}>Münsterland</span>
        <span className="srch__region" style={{ left: '28%', top: '72%' }}>Ruhrgebiet</span>
        {pts.map(({ city, list, c }) => (
          <Link key={city} to={list.length === 1 ? ROUTES.expose(list[0].id) : `?ort=${encodeURIComponent(city)}&karte=1`} className="srch__pin" style={pos(c)}
            title={list.length === 1 ? list[0].title : `${list.length} Immobilien in ${city}`}>
            <strong>{city}</strong> {list.length > 1 ? `${list.length} Objekte` : Number.isFinite(minPrice(list)) ? `${Math.round(minPrice(list) / 1000)} T€` : 'a. A.'}
          </Link>
        ))}
        <p className="srch__map-note">Schematische Darstellung – Lage nach Ort, nicht hausgenau</p>
      </div>
      {outside.length > 0 && (
        <p className="srch__map-more">Außerhalb des Kartenausschnitts: {outside.map(([city, l], i) => (
          <span key={city}>{i > 0 && ', '}<Link to={`?ort=${encodeURIComponent(city)}`} className="link-underline">{city} ({l.length})</Link></span>
        ))}</p>
      )}
    </div>
  );
}

/** Fügt nach der 5. Karte die „Suche speichern“-Promo ein (wie Referenz). */
function FragmentWithPromo({ index, children, onSave }: { index: number; children: React.ReactNode; onSave: () => void }) {
  return (
    <>
      {children}
      {index === 4 && (
        <aside className="savepromo">
          <SaveIllustration />
          <p className="savepromo__title head">Seien Sie schneller informiert als andere</p>
          <p className="savepromo__text">Speichern Sie Ihre Suche, um sie unter „Mein Bereich“ jederzeit wieder aufzurufen.</p>
          <button type="button" className="btn btn--accent btn--icon" onClick={onSave}><IconBell />Suche speichern</button>
        </aside>
      )}
    </>
  );
}

const SaveIllustration = () => (
  <svg width="120" height="100" viewBox="0 0 120 100" fill="none" stroke="#8c8c8c" strokeWidth="1" aria-hidden="true">
    <path d="M58 92V38l22-14 22 14v54M64 92V70h10v22M66 46h8v8h-8zM86 46h8v8h-8zM86 64h8v8h-8z" />
    <path d="M20 92h90" /><path d="M34 92V44" stroke="#666" />
    <rect x="18" y="44" width="40" height="26" fill="#fff" stroke="#666" />
    <rect x="22" y="56" width="32" height="8" fill="var(--c-accent)" stroke="none" />
    <path d="M24 50h22" />
  </svg>
);
