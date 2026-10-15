// Immopedia: Glossar mit ~2.000 Begriffen der bisherigen Website. Daten werden bei Bedarf aus /data/immopedia geladen.
import { useEffect, useMemo, useState } from 'react';
import { Link, useParams, useSearchParams } from 'react-router-dom';
import type { RichBlock } from '../../data/oberholz';
import { photos } from '../../data/content';
import { ROUTES } from '../../data/routes';
import { usePageMeta } from '../../layout/PageMeta';
import PageHero from '../../components/PageHero/PageHero';
import Rich from '../../components/Rich/Rich';
import Contact from '../../components/Contact/Contact';
import { IconArrowRight, IconSearch } from '../../components/Icons';
import NotFound from '../NotFound';
import { TeaserBand, TOOL_TEASERS } from './shared';
import './Immopedia.css';

type Entry = { slug: string; term: string; short: string };
let indexCache: Promise<Entry[]> | null = null;
const loadIndex = () => (indexCache ??= fetch('/data/immopedia/index.json').then((r) => r.json() as Promise<Entry[]>));

const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
const letterOf = (t: string) => {
  const c = norm(t.trim()[0] ?? '#').toUpperCase();
  return /[A-Z]/.test(c) ? c : '#';
};
const LETTERS = ['#', ...'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')];

function useIndex() {
  const [list, setList] = useState<Entry[] | null>(null);
  const [error, setError] = useState(false);
  useEffect(() => { loadIndex().then(setList).catch(() => setError(true)); }, []);
  return { list, error };
}

export function Immopedia() {
  usePageMeta({ title: 'Immopedia – Wissenslexikon für Immobilien', crumbs: [{ label: 'Immopedia' }], footer: 'accordion', description: 'Immopedia: rund 2.000 Fachbegriffe rund um Immobilienkauf, -verkauf, Finanzierung, Bewertung und Recht – kurz und verständlich erklärt von Oberholz Immobilien.' });
  const { list, error } = useIndex();
  const [qs, setQs] = useSearchParams();
  const q = qs.get('q') ?? '';
  const letter = qs.get('buchstabe') ?? (q ? '' : 'A');

  const counts = useMemo(() => {
    const m = new Map<string, number>();
    list?.forEach((e) => m.set(letterOf(e.term), (m.get(letterOf(e.term)) ?? 0) + 1));
    return m;
  }, [list]);
  const shown = useMemo(() => {
    if (!list) return [];
    if (q.trim()) {
      const n = norm(q.trim());
      const hits = list.filter((e) => norm(e.term).includes(n));
      return hits.sort((a, b) => Number(!norm(a.term).startsWith(n)) - Number(!norm(b.term).startsWith(n)) || a.term.localeCompare(b.term, 'de'));
    }
    return list.filter((e) => letterOf(e.term) === letter);
  }, [list, q, letter]);

  return (
    <>
      <PageHero eyebrow="Immopedia" title="Fachbegriffe rund um Immobilienkauf und -verkauf einfach erklärt" image={photos.advisorG} cutout
        text="Ob Grundschuld, Teilungserklärung oder Vorkaufsrecht: Immopedia ist unser digitales Nachschlagewerk mit kompakten Erklärungen zu Kauf, Verkauf, Finanzierung, Bewertung und Recht."
        checks={['Alle wichtigen Begriffe rund um Immobilienkauf und -verkauf', 'Kurz, klar & verständlich erklärt', 'Laufend aktualisiert & kostenlos nutzbar']} />
      <section className="wrap ipedia">
        <form className="ipedia__search" role="search" onSubmit={(e) => e.preventDefault()}>
          <IconSearch />
          <input value={q} onChange={(e) => { const n = new URLSearchParams(); if (e.target.value) n.set('q', e.target.value); setQs(n, { replace: true }); }}
            placeholder={list ? `In ${list.length.toLocaleString('de-DE')} Begriffen suchen …` : 'Begriffe werden geladen …'} aria-label="Begriff suchen" />
        </form>
        <nav className="ipedia__az" aria-label="Alphabet">
          {LETTERS.map((l) => (
            <button key={l} type="button" disabled={!counts.get(l)} aria-current={!q && letter === l ? 'true' : undefined}
              className={!q && letter === l ? 'is-active' : ''} onClick={() => setQs(new URLSearchParams({ buchstabe: l }))}>{l}</button>
          ))}
        </nav>
        {error && <p className="ipedia__msg">Das Lexikon konnte nicht geladen werden. Bitte laden Sie die Seite neu.</p>}
        {!list && !error && <p className="ipedia__msg">Begriffe werden geladen …</p>}
        {list && (
          <>
            <p className="ipedia__count">{q ? `${shown.length} Treffer für „${q}“` : `${shown.length} Begriffe unter ${letter}`}</p>
            <ul className="ipedia__list">
              {shown.slice(0, 300).map((e) => (
                <li key={e.slug}>
                  <Link to={ROUTES.begriff(e.slug)}>
                    <span className="ipedia__term head">{e.term}</span>
                    <span className="ipedia__short">{e.short.replace(/\s+\S*$/, '')} …</span>
                    <IconArrowRight size={18} />
                  </Link>
                </li>
              ))}
            </ul>
            {shown.length > 300 && <p className="ipedia__msg">Bitte grenzen Sie Ihre Suche weiter ein.</p>}
          </>
        )}
      </section>
      <TeaserBand items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung, TOOL_TEASERS.wertHebel]} />
      <Contact variant="page" />
    </>
  );
}

export function Begriff() {
  const { slug = '' } = useParams();
  const [data, setData] = useState<{ term: string; blocks: RichBlock[] } | null | 'missing'>(null);
  const { list } = useIndex();
  useEffect(() => {
    setData(null);
    fetch(`/data/immopedia/${encodeURIComponent(slug)}.json`)
      .then((r) => (r.ok && r.headers.get('content-type')?.includes('json') ? r.json() : Promise.reject()))
      .then(setData).catch(() => setData('missing'));
  }, [slug]);
  const term = data && data !== 'missing' ? data.term : slug;
  const firstText = data && data !== 'missing' ? (data.blocks.find((b) => b.t === 'p') as { text?: string } | undefined)?.text : undefined;
  usePageMeta({ title: `${term} – Immopedia`, crumbs: [{ label: 'Immopedia', to: ROUTES.immopedia }, { label: term }], footer: 'accordion', description: firstText?.slice(0, 158), jsonLd: data && data !== 'missing' ? [{ '@context': 'https://schema.org', '@type': 'DefinedTerm', name: data.term, description: firstText, inDefinedTermSet: 'Immopedia – Oberholz Immobilien' }] : [] });

  const neighbours = useMemo(() => {
    if (!list) return [];
    const i = list.findIndex((e) => e.slug === slug);
    return i < 0 ? [] : [list[i - 1], list[i + 1]].filter(Boolean);
  }, [list, slug]);

  if (data === 'missing') return <NotFound />;
  return (
    <>
      <header className="article__head">
        <p className="eyebrow"><Link to={ROUTES.immopedia} className="link-underline">Immopedia</Link> · Begriff</p>
        <h1 className="article__title head">{data ? data.term : ' '}</h1>
      </header>
      {data ? <div className="ipedia__body"><Rich blocks={data.blocks} /></div> : <p className="ipedia__msg wrap">Wird geladen …</p>}
      {neighbours.length > 0 && (
        <nav className="wrap ipedia__nav" aria-label="Weitere Begriffe">
          {neighbours.map((n) => <Link key={n.slug} to={ROUTES.begriff(n.slug)} className="btn btn--outline btn--small">{n.term}</Link>)}
          <Link to={`${ROUTES.immopedia}?buchstabe=${letterOf(data ? data.term : 'A')}`} className="btn btn--small">Alle Begriffe</Link>
        </nav>
      )}
      <Contact variant="page" />
    </>
  );
}
