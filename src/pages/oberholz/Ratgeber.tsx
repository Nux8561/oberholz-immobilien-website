// Ratgeber, Artikel, Leitfäden (Whitepaper) und Downloads – Inhalte der bisherigen Website.
import { Link, useParams } from 'react-router-dom';
import { articles, CATEGORIES, categoryOf, downloadGroups, downloadsIntro, findArticle, findWhitepaper, formatDate, whitepapers, type Article } from '../../data/oberholz';
import { canonicalPageUrl, ROUTES } from '../../data/routes';
import { brand, faceOf, team } from '../../data/content';
import { AUTHOR_BIO } from '../../data/ratgeber/authors';
import { faqLd, usePageMeta } from '../../layout/PageMeta';
import { SITE_URL } from '../../data/routes';
import Rich, { clean, FaqBlock } from '../../components/Rich/Rich';
import Contact from '../../components/Contact/Contact';
import SectionIntro from '../../components/SectionIntro/SectionIntro';
import { IconArrowRight, IconCheck } from '../../components/Icons';
import { LineIcon } from '../../blocks/LineIcons';
import { notify } from '../../components/Toast/Toast';
import NotFound from '../NotFound';
import { TeaserBand, TOOL_TEASERS } from './shared';

const slugify = (s: string) => s.toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const articleLd = (a: Article) => ({
  '@context': 'https://schema.org', '@type': 'Article',
  headline: a.title, description: a.subtitle, image: `${SITE_URL}${a.image}`,
  datePublished: a.date, dateModified: a.date, inLanguage: 'de-DE',
  author: { '@type': 'Person', name: a.author, worksFor: { '@id': `${SITE_URL}/#organisation` } },
  publisher: { '@id': `${SITE_URL}/#organisation` },
  mainEntityOfPage: canonicalPageUrl(ROUTES.artikel(a.slug)),
});

function PostCard({ a }: { a: Article }) {
  return (
    <Link to={ROUTES.artikel(a.slug)} className="post">
      <span className="post__img"><img src={a.thumb} alt={a.imageAlt} loading="lazy" /></span>
      <span className="post__meta">{categoryOf(a.category)?.label} · {a.readingTime} Min. Lesezeit</span>
      <h3 className="post__title head">{clean(a.title)}</h3>
      <p className="post__text">{a.subtitle}</p>
      <Byline a={a} />
    </Link>
  );
}

function Byline({ a }: { a: Article }) {
  return <span className="byline"><img src={faceOf(a.author) ?? a.authorImage} alt="" /><span><strong>{a.author}</strong>{formatDate(a.date)}</span></span>;
}

/** Autorenbox am Artikelende (wie ein Profil): Foto, Rolle, Kurzprofil, Kontakt */
function AuthorBox({ a }: { a: Article }) {
  const m = team.find((t) => t.name === a.author);
  if (!m) return null;
  return (
    <aside className="author-box">
      <img src={m.face} alt={m.name} />
      <div>
        <p className="eyebrow">Über {m.name.split(' ')[0] === 'Lubka' ? 'die Autorin' : 'den Autor'}</p>
        <p className="author-box__name head">{m.name}</p>
        <p className="author-box__role">{m.role} · {brand.name}</p>
        <p className="author-box__bio">{AUTHOR_BIO[m.name]}</p>
        <p className="author-box__links">
          <a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a> · <Link to={ROUTES.kontakt} className="link-underline">Nachricht schreiben</Link> · <Link to={ROUTES.team} className="link-underline">Zum Team</Link>
        </p>
      </div>
    </aside>
  );
}

function CategoryNav({ active }: { active?: string }) {
  return (
    <nav className="cat-nav" aria-label="Ratgeber-Kategorien">
      <Link to={ROUTES.ratgeber} className={`chip${!active ? ' is-active' : ''}`}>Alle Themen</Link>
      {CATEGORIES.map((c) => <Link key={c.slug} to={ROUTES.ratgeberThema(c.slug)} className={`chip${active === c.slug ? ' is-active' : ''}`}>{c.label}</Link>)}
    </nav>
  );
}

/** Leitfäden und Dokumente zum Download (früher eigene Seite „Dokumente & Downloads“) */
function Downloads() {
  return (
    <section className="wrap" id="downloads" style={{ scrollMarginTop: 140 }}>
      <SectionIntro variant="inline" line={false} eyebrow="Leitfäden & Downloads" title="Leitfäden, Formulare und Merkblätter" text={downloadsIntro} />
      <div className="dl-group">
        <h3 className="rich__h3 head" style={{ marginTop: 0 }}>Kostenlose PDF-Leitfäden</h3>
        <div className="dl-list">
          {whitepapers.map((w) => (
            <Link key={w.slug} to={ROUTES.whitepaper(w.slug)} className="dl">
              <LineIcon name="academy" size={32} />
              <span><span className="dl__title">{clean(w.title)}</span><span className="dl__text">{w.facts}</span><span className="dl__meta">Zum kostenlosen PDF <IconArrowRight size={14} /></span></span>
            </Link>
          ))}
        </div>
      </div>
      {downloadGroups.map((g) => (
        <div key={g.title} className="dl-group">
          <h3 className="rich__h3 head" style={{ marginTop: 0 }}>{g.title}</h3>
          <div className="dl-list">
            {g.items.map((d) => (
              <a key={d.href} href={d.href} className="dl" download>
                <LineIcon name="document" size={32} />
                <span><span className="dl__title">{d.title}</span><span className="dl__text">{d.text}</span><span className="dl__meta">PDF · {d.size} · Herunterladen</span></span>
              </a>
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}

/** Ratgeber-Startseite: Top-Beitrag, Kategorien mit je drei Beiträgen, Leitfäden. */
export function Ratgeber() {
  usePageMeta({ title: 'Immobilien-Ratgeber: Wissen für Käufer, Verkäufer und Eigentümer', crumbs: [{ label: 'Ratgeber' }], footer: 'accordion', description: 'Der Immobilien-Ratgeber von Oberholz Immobilien: Kaufnebenkosten, Ablauf beim Hauskauf, Immobilienbewertung, Verkauf, Vermietung, Erbe und Steuern – verständlich erklärt.' });
  const [top] = articles;
  return (
    <>
      <SectionIntro level="h1" eyebrow="Ratgeber" title="Ihr Immobilien-Ratgeber – Wissen, Tipps und Entscheidungshilfen"
        text="Fundierte Beiträge für Käufer, Verkäufer, Eigentümer und Erben: verständlich erklärt, mit Beispielrechnungen und Checklisten – von unserem Team aus Maklern und Gutachtern." />
      <div className="wrap" style={{ paddingTop: 0, paddingBottom: 24 }}><CategoryNav /></div>
      <section className="wrap" style={{ paddingTop: 0 }}>
        <Link to={ROUTES.artikel(top.slug)} className="feature">
          <span className="feature__img"><img src={top.image} alt={top.imageAlt} /></span>
          <span className="feature__body">
            <span className="post__meta">{categoryOf(top.category)?.label} · {top.readingTime} Min. Lesezeit</span>
            <span className="feature__title head">{clean(top.title)}</span>
            <span className="post__text">{top.subtitle}</span>
            <Byline a={top} />
            <span className="btn feature__cta">Weiterlesen</span>
          </span>
        </Link>
      </section>
      {CATEGORIES.map((c) => {
        const list = articles.filter((a) => a.category === c.slug && a.slug !== top.slug);
        return (
          <section key={c.slug} className="wrap">
            <SectionIntro variant="inline" line={false} eyebrow={c.label} title={c.title} text={c.text} />
            <div className="posts">{list.slice(0, 3).map((a) => <PostCard key={a.slug} a={a} />)}</div>
            <div className="srch__center"><Link to={ROUTES.ratgeberThema(c.slug)} className="btn btn--outline">Alle {list.length + (top.category === c.slug ? 1 : 0)} Beiträge für {c.label}</Link></div>
          </section>
        );
      })}
      <TeaserBand id="rechner" items={[TOOL_TEASERS.budget, TOOL_TEASERS.finanzierung, TOOL_TEASERS.wertHebel]} />
      <Downloads />
      <Contact variant="page" />
    </>
  );
}

export function RatgeberThema() {
  const { cat = '' } = useParams();
  const c = categoryOf(cat);
  usePageMeta(c ? { title: `Ratgeber: ${c.title}`, crumbs: [{ label: 'Ratgeber', to: ROUTES.ratgeber }, { label: c.label }], footer: 'accordion', description: c.text } : { title: 'Thema nicht gefunden', noindex: true });
  if (!c) return <NotFound />;
  const list = articles.filter((a) => a.category === c.slug);
  return (
    <>
      <SectionIntro level="h1" eyebrow="Ratgeber" title={c.title} text={c.text} />
      <div className="wrap" style={{ paddingTop: 0, paddingBottom: 24 }}><CategoryNav active={c.slug} /></div>
      <section className="wrap" style={{ paddingTop: 0 }}><div className="posts">{list.map((a) => <PostCard key={a.slug} a={a} />)}</div>
        <div className="srch__center"><Link to={ROUTES.downloads} className="btn btn--outline">Leitfäden & Downloads</Link></div></section>
      <Contact variant="page" />
    </>
  );
}

export function Artikel() {
  const { slug = '' } = useParams();
  const a = findArticle(slug);
  usePageMeta(a ? { title: a.title, crumbs: [{ label: 'Ratgeber', to: ROUTES.ratgeber }, { label: categoryOf(a.category)?.label ?? '', to: ROUTES.ratgeberThema(a.category) }, { label: a.title }], footer: 'accordion', description: a.subtitle, image: a.image, jsonLd: [articleLd(a), ...(a.faq.length ? [faqLd(a.faq)] : [])] } : { title: 'Beitrag nicht gefunden', noindex: true });
  if (!a) return <NotFound />;
  const wp = a.whitepaper ? findWhitepaper(a.whitepaper) : undefined;
  const share = async () => {
    try {
      if (navigator.share) await navigator.share({ title: a.title, url: window.location.href });
      else { await navigator.clipboard.writeText(window.location.href); notify('Link in die Zwischenablage kopiert.'); }
    } catch { /* abgebrochen */ }
  };
  const related = [...articles.filter((x) => x.slug !== a.slug && x.category === a.category), ...articles.filter((x) => x.category !== a.category)].slice(0, 3);
  const cat = categoryOf(a.category);
  return (
    <>
      <header className="article__head">
        <p className="post__meta"><Link to={ROUTES.ratgeberThema(a.category)} className="link-underline">{cat?.label}</Link> · {a.readingTime} Min. Lesezeit · {formatDate(a.date)}</p>
        <h1 className="article__title head">{clean(a.title)}</h1>
        <p className="article__sub">{a.subtitle}</p>
        <Byline a={a} />
      </header>
      <figure className="article__hero"><img src={a.image} alt={a.imageAlt} /></figure>
      <div className="rich">
        <div className="rich__text">
          <p className="rich__p article__intro" style={{ marginTop: 40 }}>{a.intro}</p>
          {a.facts.length > 0 && (
            <aside className="facts">
              <p className="eyebrow">Das Wichtigste in Kürze</p>
              <ul className="rich__checks">{a.facts.map((f) => <li key={f}><span className="rich__tick"><IconCheck size={14} /></span><span>{f}</span></li>)}</ul>
            </aside>
          )}
          <details className="toc" open>
            <summary className="eyebrow">Inhaltsverzeichnis</summary>
            <ol>{a.toc.map((t) => <li key={t}><a href={`#${slugify(t)}`} onClick={(e) => { e.preventDefault(); document.getElementById(slugify(t))?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>{t}</a></li>)}</ol>
          </details>
        </div>
      </div>
      <ArticleBody blocks={a.body} />
      {['erst-sanieren-dann-verkaufen-was-sich-wirklich-rechnet', 'der-grosse-generationenwechsel-was-der-silver-tsunami-fuer-immobilienverkaeufer-bedeutet'].includes(a.slug) && <aside className="owner-sources" aria-label="Quelle zum energetischen Zustand"><p className="eyebrow">Markteinordnung</p><p><a className="link-underline" href="https://www.immowelt.de/ueberuns/presse/pressemitteilungenkontakt/immoweltde/2026/gute-energiebilanz-zahlt-sich-aus-bis-zu-20-prozent-preisaufschlag-fuer-effiziente-immobilien/" target="_blank" rel="noopener noreferrer">immowelt-Auswertung vom 19. März 2026: Energieeffizienz und Angebotspreise</a></p></aside>}

      <div className="rich"><div className="rich__text"><AuthorBox a={a} /></div></div>
      {a.faq.length > 0 && <div className="rich"><div className="rich__text"><FaqBlock title={`Häufige Fragen: ${clean(a.title).split(':')[0]}`} items={a.faq} /></div></div>}
      {a.tools.length > 0 && <TeaserBand items={a.tools.map((t) => TOOL_TEASERS[t])} />}
      {wp && (
        <section className="wrap">
          <div className="lead">
            <img className="lead__img" src={a.image} alt="" />
            <div>
              <p className="eyebrow">Leitfaden zum Download</p>
              <h2 className="rich__h2 head" style={{ marginTop: 8 }}>{clean(wp.title)}</h2>
              <p className="rich__p">{wp.intro}</p>
              <Link to={ROUTES.whitepaper(wp.slug)} className="btn btn--accent">Zum kostenlosen PDF</Link>
            </div>
          </div>
        </section>
      )}
      <div className="rich"><div className="rich__text">
        <div className="share">Teilen:
          <button type="button" className="link-underline" onClick={share}>Link teilen</button>
          <a className="link-underline" href={`mailto:?subject=${encodeURIComponent(a.title)}&body=${encodeURIComponent(window.location.href)}`}>Per E-Mail</a>
          <a className="link-underline" href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`} target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </div>
      </div></div>
      <section className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow={cat?.label} title="Weitere Beiträge" />
        <div className="posts">{related.map((x) => <PostCard key={x.slug} a={x} />)}</div>
        <div className="srch__center"><Link to={ROUTES.ratgeberThema(a.category)} className="btn btn--outline">Alle Beiträge für {cat?.label}</Link></div>
      </section>
      <Contact variant="page" />
    </>
  );
}

/** Artikeltext mit Ankern an den Kapitelüberschriften */
function ArticleBody({ blocks }: { blocks: Article['body'] }) {
  return (
    <div ref={(el) => {
      if (!el) return;
      el.querySelectorAll('h2').forEach((h) => { if (!h.id) h.id = slugify(h.textContent ?? ''); h.style.scrollMarginTop = '140px'; });
    }}>
      <Rich blocks={blocks} />
    </div>
  );
}

export function Whitepaper() {
  const { slug = '' } = useParams();
  const w = findWhitepaper(slug);
  usePageMeta(w ? { title: w.title, crumbs: [{ label: 'Ratgeber', to: ROUTES.ratgeber }, { label: 'Leitfäden', to: ROUTES.downloads }, { label: w.title }], footer: 'accordion', description: w.intro, image: w.image } : { title: 'Leitfaden nicht gefunden', noindex: true });
  if (!w) return <NotFound />;
  return (
    <>
      <section className="wrap" style={{ paddingTop: 48 }}>
        <div className="lead">
          <div>
            <p className="eyebrow">Kostenloser Leitfaden · {w.facts}</p>
            <h1 className="article__title head" style={{ margin: '8px 0 16px' }}>{clean(w.title)}</h1>
            <p className="rich__p">{w.intro}</p>
            <ul className="rich__checks">{w.items.map((x) => <li key={x}><span className="rich__tick"><IconCheck size={14} /></span><span>{clean(x)}</span></li>)}</ul>
            {w.article && <img className="lead__img" src={w.article.image} alt={w.article.imageAlt} />}
          </div>
          <aside className="lead__box" id="anfordern">
            <p className="eyebrow">Direkt herunterladen</p>
            <h2 className="head guide-download-title">Ihr Ratgeber zum Mitnehmen</h2>
            <p className="rich__p">Die PDF-Lesefassung des zugehörigen Ratgeberbeitrags können Sie kostenlos speichern und ausdrucken.</p>
            <a href={w.file.href} className="btn btn--accent btn--icon" download><LineIcon name="document" size={20} />PDF herunterladen</a>
            <p className="guide-download-meta">{w.file.pages} Seiten · PDF · {w.file.sizeKB} KB</p>
            <p className="rich__p">Sie haben Fragen zu Ihrer eigenen Immobilie?</p>
            <Link to={ROUTES.kontakt} className="link-underline">Persönliches Gespräch anfragen</Link>
          </aside>
        </div>
      </section>
      {w.article && (
        <section className="wrap">
          <SectionIntro variant="inline" line={false} eyebrow="Passender Ratgeber-Beitrag" title={clean(w.article.title)} text={w.article.subtitle} />
          <div className="srch__center" style={{ marginTop: 0 }}><Link to={ROUTES.artikel(w.article.slug)} className="btn btn--outline">Beitrag lesen</Link></div>
        </section>
      )}
      <Contact variant="page" />
    </>
  );
}


