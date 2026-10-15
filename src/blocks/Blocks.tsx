// Baustein-Bibliothek für die Unterseiten-Templates. Jeder Block entspricht einem in der Referenz
// wiederkehrenden Abschnitt (Maße: analysis/engelvoelkers/pages/*_1440.txt).
import { useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { properties, type Property } from '../data/properties';
import SectionIntro from '../components/SectionIntro/SectionIntro';
import SplitCard from '../components/SplitCard/SplitCard';
import PropertyCard from '../components/PropertyCard/PropertyCard';
import Accordion from '../components/Accordion/Accordion';
import Contact from '../components/Contact/Contact';
import Deco from '../components/Deco/Deco';
import PropertySearch from '../components/PropertySearch/PropertySearch';
import { LifestyleGrid } from '../components/LifestyleGallery/LifestyleGallery';
import { BenefitIcon, IconArrowRight, IconChevronDown, IconChevronLeft, IconChevronRight, IconMail } from '../components/Icons';
import { LineIcon, type LineIconName } from './LineIcons';
import './Blocks.css';

export type Btn = { label: string; to: string; variant?: 'primary' | 'outline' | 'accent' | 'accentDark'; icon?: 'mail' | 'phone' };

export type Block =
  | { type: 'splitHero'; title: string; text?: string; image: string; alt?: string; buttons?: Btn[]; search?: boolean }
  | { type: 'wideHero'; image: string; alt: string }
  | { type: 'image'; image: string; alt: string; ratio?: string }
  | { type: 'intro'; eyebrow?: string; title: string; text?: string; line?: boolean; level?: 'h1' | 'h2'; cta?: Btn }
  | { type: 'benefits'; items: { icon: LineIconName; title: string; text: string }[] }
  | { type: 'stats'; items: { icon: LineIconName; label: string; value: string }[] }
  | { type: 'split'; image: string; alt: string; title: string; text: string; cta: Btn; tone?: 'cream' | 'grey' }
  | { type: 'steps'; items: { icon: LineIconName; label: string; title: string; text: string; image: string }[]; variant?: 'steps' | 'services' }
  | { type: 'gallery'; items: { image: string; title: string; alt: string }[] }
  | { type: 'faq'; eyebrow?: string; title: string; items: { q: string; a: string }[] }
  | { type: 'regions'; eyebrow?: string; title: string; text?: string; items: { title: string; links: { label: string; to: string }[] }[] }
  | { type: 'info'; title: string; text: string; icon: LineIconName }
  | { type: 'profile'; title: string; items: { title: string; text: string }[]; image: string; alt: string; text?: string; cta?: Btn }
  | { type: 'textImage'; title: string; text: string; image: string; alt: string; cta?: Btn; tone?: 'grey' | 'white' }
  | { type: 'quotes'; items: { quote: string; name: string; role: string; image?: string }[] }
  | { type: 'tiles'; items: { image: string; title: string; text?: string; to: string }[]; cta?: Btn; columns?: 2 | 3 }
  | { type: 'timeline'; items: { image: string; title: string; text: string }[]; visible?: number }
  | { type: 'properties'; eyebrow?: string; title: string; text?: string; filter: (p: Property) => boolean; fallback?: boolean; tabs?: boolean; cta?: Btn; tone?: 'grey' }
  | { type: 'reports'; eyebrow?: string; title: string; text?: string; items: { image: string; title: string; sub: string; to: string }[]; cta?: Btn }
  | { type: 'shopInfo'; eyebrow: string; title: string; image: string; lines: ReactNode[]; buttons: Btn[] }
  | { type: 'linkColumns'; eyebrow?: string; title: string; items: { label: string; to: string }[]; initial?: number }
  | { type: 'contact' } | { type: 'deco' } | { type: 'custom'; render: () => ReactNode };

export function Button({ b, className = '' }: { b: Btn; className?: string }) {
  const cls = `btn${b.variant === 'outline' ? ' btn--outline' : b.variant === 'accent' ? ' btn--accent' : b.variant === 'accentDark' ? ' btn--accent-dark' : ''}${b.icon ? ' btn--icon' : ''} ${className}`;
  const icon = b.icon === 'mail' ? <IconMail /> : b.icon === 'phone' ? <LineIcon name="phone" size={24} /> : null;
  if (b.to && /^(tel:|mailto:|https?:)/.test(b.to)) return <a href={b.to} className={cls} {...(b.to.startsWith('http') ? { target: '_blank', rel: 'noopener noreferrer' } : {})}>{icon}{b.label}</a>;
  return <Link to={b.to} className={cls}>{icon}{b.label}</Link>;
}

/* ---------- einzelne Blöcke ---------- */

function SplitHero(b: Extract<Block, { type: 'splitHero' }>) {
  return (
    <section className="b-shero">
      <div className="b-shero__grid">
        <article className="b-shero__body">
          <p className="b-shero__title head">{b.title}</p>
          {b.text && <p className="b-shero__text">{b.text}</p>}
          {b.search && <div className="b-shero__search"><PropertySearch /></div>}
          {b.buttons && <div className="b-shero__btns">{b.buttons.map((x) => <Button key={x.label} b={x} />)}</div>}
        </article>
        <div className="b-shero__media"><img src={b.image} alt={b.alt ?? ''} /></div>
      </div>
    </section>
  );
}

function Benefits({ items }: { items: { icon: LineIconName; title: string; text: string }[] }) {
  return (
    <div className="wrap">
      <ul className={`b-benefits b-benefits--${items.length}`}>
        {items.map((it) => (
          <li key={it.title}><LineIcon name={it.icon} size={48} /><h2 className="head">{it.title}</h2><p>{it.text}</p></li>
        ))}
      </ul>
    </div>
  );
}

function Stats({ items }: { items: { icon: LineIconName; label: string; value: string }[] }) {
  return (
    <div className="wrap">
      <ul className={`b-stats${items.length > 3 ? ' b-stats--wrap' : ''}`}>
        {items.map((it) => <li key={it.label}><LineIcon name={it.icon} size={32} /><p className="eyebrow">{it.label}</p><p className="head">{it.value}</p></li>)}
      </ul>
    </div>
  );
}

function Steps({ items, variant = 'steps' }: { items: Extract<Block, { type: 'steps' }>['items']; variant?: 'steps' | 'services' }) {
  const [i, setI] = useState(0);
  const it = items[i];
  return (
    <div className={`wrap b-steps b-steps--${variant}`}>
      <div className="b-steps__tabs" role="tablist">
        {items.map((s, k) => (
          <button key={s.label} type="button" role="tab" aria-selected={k === i} className={k === i ? 'is-active' : ''} onClick={() => setI(k)}>
            <LineIcon name={s.icon} size={32} /><span>{s.label}</span>
          </button>
        ))}
      </div>
      <div className="b-steps__slide" role="tabpanel">
        <div className="b-steps__img"><img src={it.image} alt="" /></div>
        <div className="b-steps__body"><h3 className="head">{it.title}</h3><p>{it.text}</p></div>
      </div>
      {variant === 'steps' && (
        <div className="b-steps__nav">
          <button type="button" aria-label="Vorheriger Schritt" disabled={i === 0} onClick={() => setI(i - 1)}><IconChevronLeft size={20} /></button>
          <span>{i + 1} von {items.length}</span>
          <button type="button" aria-label="Nächster Schritt" disabled={i === items.length - 1} onClick={() => setI(i + 1)}><IconChevronRight size={20} /></button>
        </div>
      )}
    </div>
  );
}

function Info({ title, text, icon }: { title: string; text: string; icon: LineIconName }) {
  return (
    <div className="wrap"><aside className="b-info"><LineIcon name={icon} size={32} /><div><p className="head">{title}</p><p>{text}</p></div></aside></div>
  );
}

function Profile(b: Extract<Block, { type: 'profile' }>) {
  return (
    <section className="wrap b-profile">
      <div>
        <h2 className="b-profile__title head">{b.title}</h2>
        {b.text && <p className="b-profile__text">{b.text}</p>}
        <FaqList items={b.items.map((x) => ({ q: x.title, a: x.text }))} />
        {b.cta && <div className="b-profile__cta"><Button b={b.cta} /></div>}
      </div>
      <div className="b-profile__img"><img src={b.image} alt={b.alt} loading="lazy" /></div>
    </section>
  );
}

function FaqList({ items }: { items: { q: string; a: string }[] }) {
  return <div className="b-faq"><Accordion items={items.map((x) => ({ title: x.q, content: <p>{x.a}</p> }))} /></div>;
}

function TextImage(b: Extract<Block, { type: 'textImage' }>) {
  const [open, setOpen] = useState(false);
  return (
    <section className={`b-ti b-ti--${b.tone ?? 'white'}`}>
      <div className="b-ti__inner">
        <div className="b-ti__body">
          <h2 className="head">{b.title}</h2>
          <p className={open ? 'is-open' : ''}>{b.text}</p>
          {b.text.length > 420 && <button type="button" className="b-more" onClick={() => setOpen(!open)}>{open ? 'Weniger anzeigen' : 'Mehr anzeigen'}<span className="b-more__icon">{open ? '−' : '+'}</span></button>}
          {b.cta && <div className="b-ti__cta"><Button b={{ variant: 'outline', ...b.cta }} className="btn--small" /></div>}
        </div>
        <div className="b-ti__img"><img src={b.image} alt={b.alt} loading="lazy" /></div>
      </div>
    </section>
  );
}

function Quotes({ items }: { items: { quote: string; name: string; role: string; image?: string }[] }) {
  const [i, setI] = useState(0);
  const q = items[i];
  return (
    <div className="wrap">
      <figure className="b-quote">
        <div className="b-quote__img">{q.image && <img src={q.image} alt="" />}</div>
        <div className="b-quote__body">
          <blockquote className="head">„{q.quote}“</blockquote>
          <figcaption><span>{q.name}</span><small>{q.role}</small></figcaption>
        </div>
      </figure>
      {items.length > 1 && (
        <div className="b-quote__dots">{items.map((_, k) => <button key={k} type="button" aria-label={`Zitat ${k + 1}`} className={k === i ? 'is-active' : ''} onClick={() => setI(k)} />)}</div>
      )}
    </div>
  );
}

function Tiles({ items, cta, columns = 3 }: { items: Extract<Block, { type: 'tiles' }>['items']; cta?: Btn; columns?: 2 | 3 }) {
  return (
    <div className="wrap">
      <div className={`b-tiles b-tiles--${columns}`}>
        {items.map((t) => (
          <Link key={t.title} to={t.to} className="city b-tile">
            <div className="city__media"><img src={t.image} alt="" loading="lazy" /></div>
            <div className="city__body"><h3 className="city__name head">{t.title}</h3>{t.text && <p className="city__sub">{t.text}</p>}</div>
            <span className="city__link"><IconArrowRight /></span>
          </Link>
        ))}
      </div>
      {cta && <div className="b-center"><Button b={{ variant: 'outline', ...cta }} className="btn--small" /></div>}
    </div>
  );
}

function Timeline({ items, visible = 6 }: { items: Extract<Block, { type: 'timeline' }>['items']; visible?: number }) {
  const [all, setAll] = useState(false);
  return (
    <div className="b-timeline">
      <ol>
        {(all ? items : items.slice(0, visible)).map((t) => (
          <li key={t.title}><img src={t.image} alt="" loading="lazy" /><div><h3 className="head">{t.title}</h3><p>{t.text}</p></div></li>
        ))}
      </ol>
      {items.length > visible && <div className="b-center"><button type="button" className="btn btn--outline btn--small" onClick={() => setAll(!all)}>{all ? 'Weniger anzeigen' : 'Mehr erfahren'}<IconChevronDown size={16} /></button></div>}
    </div>
  );
}

function PropertyRow(b: Extract<Block, { type: 'properties' }>) {
  const [mode, setMode] = useState<'kaufen' | 'mieten'>('kaufen');
  const inMode = (p: Property) => !b.tabs || p.mode === mode;
  let list = properties.filter((p) => b.filter(p) && inMode(p)).slice(0, 3);
  if (list.length === 0 && b.fallback) list = properties.filter(inMode).slice(0, 3); // keine Treffer im Ort → allgemeine Highlights
  return (
    <section className={`b-props${b.tone ? ' b-props--grey' : ''}`}>
      <div className="wrap">
        <SectionIntro variant="inline" line={false} eyebrow={b.eyebrow} title={b.title} text={b.text} />
        {b.tabs && (
          <div className="b-props__tabs" role="tablist">
            {(['kaufen', 'mieten'] as const).map((m) => <button key={m} type="button" role="tab" aria-selected={mode === m} className={`psearch__mode${mode === m ? ' is-selected' : ''}`} onClick={() => setMode(m)}>{m === 'kaufen' ? 'Kaufen' : 'Mieten'}</button>)}
          </div>
        )}
        <div className="expo__similar-grid">{list.map((p) => <PropertyCard key={p.id} p={p} compact />)}</div>
        {list.length === 0 && <p className="b-empty">Aktuell keine passenden Angebote.</p>}
        {b.cta && <div className="b-center"><Button b={{ variant: 'outline', ...b.cta }} className="btn--small" /></div>}
      </div>
    </section>
  );
}

function Reports(b: Extract<Block, { type: 'reports' }>) {
  return (
    <section className="wrap">
      <SectionIntro variant="inline" line={false} eyebrow={b.eyebrow} title={b.title} text={b.text} />
      <div className="b-reports">
        {b.items.map((r) => (
          <Link key={r.title} to={r.to} className="b-report">
            <span className="b-report__img"><img src={r.image} alt="" loading="lazy" /></span>
            <h3 className="head">{r.title}</h3><p>{r.sub}</p><span className="b-report__read">5 Min. Lesezeit <IconArrowRight size={16} /></span>
          </Link>
        ))}
      </div>
      {b.cta && <div className="b-center"><Button b={{ variant: 'outline', ...b.cta }} className="btn--small" /></div>}
    </section>
  );
}

function ShopInfo(b: Extract<Block, { type: 'shopInfo' }>) {
  return (
    <section className="expo__shop b-shop">
      <div className="wrap">
        <SectionIntro variant="inline" line={false} center eyebrow={b.eyebrow} title={b.title} />
        <div className="expo__shop-row">
          <img src={b.image} alt="" className="expo__shop-img" />
          <div className="expo__shop-info">{b.lines.map((l, i) => <p key={i}>{l}</p>)}</div>
        </div>
        <div className="b-center b-shop__btns">{b.buttons.map((x) => <Button key={x.label} b={x} className="btn--small" />)}</div>
      </div>
    </section>
  );
}

function LinkColumns(b: Extract<Block, { type: 'linkColumns' }>) {
  const [all, setAll] = useState(false);
  const n = b.initial ?? b.items.length;
  return (
    <section className="sintro-wrap">
      <SectionIntro variant="inline" line={false} eyebrow={b.eyebrow} title={b.title} />
      <ul className="countries">{(all ? b.items : b.items.slice(0, n)).map((l) => <li key={l.label}><Link to={l.to}>{l.label}</Link></li>)}</ul>
      {b.items.length > n && <button type="button" className="topic__more" onClick={() => setAll(!all)}>{all ? 'Weniger anzeigen' : 'Mehr anzeigen'}<span className="b-more__icon">{all ? '−' : '+'}</span></button>}
    </section>
  );
}

export function RenderBlocks({ blocks }: { blocks: Block[] }) {
  return (
    <>
      {blocks.map((b, i) => {
        switch (b.type) {
          case 'splitHero': return <SplitHero key={i} {...b} />;
          case 'wideHero': return <div key={i} className="b-wide"><img src={b.image} alt={b.alt} /></div>;
          case 'intro': return (
            <div key={i} className={b.cta ? 'b-intro-cta' : ''}>
              <SectionIntro level={b.level} line={b.line ?? true} eyebrow={b.eyebrow} title={b.title} text={b.text} />
              {b.cta && <div className="b-center b-intro-cta__btn"><Button b={b.cta} className="btn--small" /></div>}
            </div>
          );
          case 'benefits': return <Benefits key={i} items={b.items} />;
          case 'stats': return <Stats key={i} items={b.items} />;
          case 'split': return <div key={i} className={b.tone === 'grey' ? 'b-split--grey' : ''}><SplitCard image={b.image} alt={b.alt} title={b.title} text={b.text} cta={b.cta.label} to={b.cta.to ?? null} /></div>;
          case 'steps': return <Steps key={i} items={b.items} variant={b.variant} />;
          case 'gallery': return <LifestyleGrid key={i} items={b.items} />;
          case 'faq': return (
            <section key={i} className="sintro-wrap b-faq-sec">
              <SectionIntro variant="inline" line={false} eyebrow={b.eyebrow ?? 'FAQ'} title={b.title} />
              <FaqList items={b.items} />
            </section>
          );
          case 'regions': return (
            <section key={i} className="wrap b-regions">
              <SectionIntro variant="inline" line={false} eyebrow={b.eyebrow} title={b.title} text={b.text} />
              <Accordion columns={2} items={b.items.map((r) => ({ title: r.title, content: <ul className="region-links">{r.links.map((l) => <li key={l.label}><Link to={l.to}>{l.label}</Link></li>)}</ul> }))} />
            </section>
          );
          case 'info': return <Info key={i} {...b} />;
          case 'profile': return <Profile key={i} {...b} />;
          case 'textImage': return <TextImage key={i} {...b} />;
          case 'quotes': return <Quotes key={i} items={b.items} />;
          case 'tiles': return <Tiles key={i} items={b.items} cta={b.cta} columns={b.columns} />;
          case 'image': return <div key={i} className="b-image"><img src={b.image} alt={b.alt} style={{ aspectRatio: b.ratio ?? '3 / 2' }} loading="lazy" /></div>;
          case 'timeline': return <Timeline key={i} items={b.items} visible={b.visible} />;
          case 'properties': return <PropertyRow key={i} {...b} />;
          case 'reports': return <Reports key={i} {...b} />;
          case 'shopInfo': return <ShopInfo key={i} {...b} />;
          case 'linkColumns': return <LinkColumns key={i} {...b} />;
          case 'contact': return <Contact key={i} />;
          case 'deco': return <Deco key={i} />;
          case 'custom': return <div key={i}>{b.render()}</div>;
          default: return null;
        }
      })}
    </>
  );
}

export { BenefitIcon };
