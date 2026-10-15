// Darstellung der übernommenen Seiteninhalte (content.json) im Stil der Seiten-Templates:
// Fließtext auf 896px, wiederkehrende Muster (Teamleiste, Vergleichstabelle, Schrittfolgen,
// Spaltenlisten, FAQ, Downloads) werden automatisch erkannt und als eigene Bausteine gerendert.
import { Fragment, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import type { QA, RichBlock } from '../../data/oberholz';
import { brand, faceOf, reviewFaces } from '../../data/content';
import { ROUTES } from '../../data/routes';
import Accordion from '../Accordion/Accordion';
import Stars from '../Stars/Stars';
import { openRatings } from '../RatingPanel/RatingPanel';
import { IconArrowRight, IconCheck, IconClose } from '../Icons';
import './Rich.css';

type Img = Extract<RichBlock, { t: 'img' }>;
type Node =
  | { k: 'block'; b: RichBlock }
  | { k: 'eyebrow'; text: string }
  | { k: 'team'; imgs: Img[] }
  | { k: 'advisor'; img: Img }
  | { k: 'faces' }
  | { k: 'columns'; items: { title: string; items: string[] }[] }
  | { k: 'steps'; title: string; items: { title: string; text: string }[] }
  | { k: 'faq'; title: string; items: QA[] }
  | { k: 'brochure'; href: string; images: string[] };

const isTeamImg = (b: RichBlock): boolean => b.t === 'img' && /bannerright-1440\/t7a|oberholz-team/.test(b.src);
const isFace = (b: RichBlock) => b.t === 'img' && /headbanner-testimonials|facepile|videocard_avatar/.test(b.src);
const isCaps = (s: string) => /[A-ZÄÖÜ]/.test(s) && s === s.toUpperCase();
/** Tippfehler/Platzhalter der Quelle bereinigen */
export const clean = (s: string) => s
  .replace(/Immobilienberaterin(?:in)+/g, 'Immobilienberaterin')
  .replace(/unsere hauseigene Werbeagentur unser Vermarktungsansatz/gi, 'unsere hauseigene Werbeagentur')
  .replace(/Unsere hauseigene Werbeagentur unser Vermarktungsansatz/g, 'Unsere hauseigene Werbeagentur')
  .replace(/der Oberholz Immobilien der Oberholz Immobilien/g, 'der Oberholz Immobilien')
  .replace(/lückenhaftte/g, 'lückenhafte');
export const personOf = (alt: string) => {
  const [name, role] = clean(alt).split(' - ');
  return { name, role: role ?? '' };
};

function parse(blocks: RichBlock[], faqFallback: QA[]): Node[] {
  const out: Node[] = [];
  let i = 0;
  const at = (k: number) => blocks[k];
  while (i < blocks.length) {
    const b = at(i);
    // Teamleiste bzw. einzelne Berater:innen-Karte
    if (isTeamImg(b)) {
      const imgs: Img[] = [];
      while (i < blocks.length && isTeamImg(at(i))) imgs.push(at(i++) as Img);
      out.push(imgs.length > 1 ? { k: 'team', imgs } : { k: 'advisor', img: imgs[0] });
      continue;
    }
    if (isFace(b)) {
      let n = 0;
      while (i < blocks.length && isFace(at(i))) { i++; n++; }
      if (n > 1) out.push({ k: 'faces' });
      continue;
    }
    // Broschüre: PDF-Link + Titelbilder
    if (b.t === 'pdf' && !b.text) {
      const images: string[] = [];
      i++;
      while (i < blocks.length && at(i).t === 'img' && /contentimg/.test((at(i) as Img).src)) images.push((at(i++) as Img).src);
      out.push({ k: 'brochure', href: b.href, images });
      continue;
    }
    if (b.t === 'h2' && /^Häufige Fragen/.test(b.text)) {
      const items: QA[] = [];
      i++;
      while (i < blocks.length && at(i).t === 'h3') {
        const q = (at(i) as { text: string }).text;
        const next = at(i + 1);
        if (next?.t === 'p') { items.push({ q, a: next.text }); i += 2; }
        else { const f = faqFallback.find((x) => x.q === q); if (f) items.push(f); i++; }
      }
      out.push({ k: 'faq', title: b.text, items });
      continue;
    }
    // drei und mehr Paare aus Überschrift + kurzer Liste → Spalten
    if (b.t === 'h2' && at(i + 1)?.t === 'ul') {
      const items: { title: string; items: string[] }[] = [];
      let k = i;
      while (at(k)?.t === 'h2' && at(k + 1)?.t === 'ul' && (at(k + 1) as { items: string[] }).items.every((x) => x.length < 90)) {
        items.push({ title: (at(k) as { text: string }).text, items: (at(k + 1) as { items: string[] }).items });
        k += 2;
      }
      if (items.length >= 3) { out.push({ k: 'columns', items }); i = k; continue; }
    }
    // Überschrift + mindestens drei kurze h3/p-Paare → Schrittfolge
    if (b.t === 'h2' && at(i + 1)?.t === 'h3') {
      const items: { title: string; text: string }[] = [];
      let k = i + 1;
      while (at(k)?.t === 'h3' && at(k + 1)?.t === 'p' && (at(k + 1) as { text: string }).text.length < 260) {
        items.push({ title: (at(k) as { text: string }).text, text: (at(k + 1) as { text: string }).text });
        k += 2;
      }
      if (items.length >= 3) { out.push({ k: 'steps', title: b.text, items }); i = k; continue; }
    }
    if (b.t === 'p') {
      if (b.text === 'Weiterlesen»' || /Landkreis Cloppenburg/.test(b.text)) { i++; continue; }
      if (isCaps(b.text)) { if (b.text.length <= 30) out.push({ k: 'eyebrow', text: b.text }); i++; continue; }
    }
    if (b.t === 'img' && /blog-thumb|focuspoint|contentimg/.test(b.src)) { i++; continue; }
    out.push({ k: 'block', b });
    i++;
  }
  return out;
}

function Compare({ rows }: { rows: string[][] }) {
  const [, ...body] = rows;
  return (
    <div className="rich__compare" role="table" aria-label="Vergleich klassischer Makler und Oberholz Immobilien">
      <div className="rich__compare-row rich__compare-head" role="row">
        <span role="columnheader" /><span role="columnheader">Klassischer Makler</span><span role="columnheader">{brand.name}</span>
      </div>
      {body.map((r, i) => (
        <div key={r[0]} className="rich__compare-row" role="row">
          <span role="rowheader">{clean(r[0])}</span>
          <span role="cell" className={i === 0 ? 'is-yes' : 'is-no'}>{i === 0 ? <IconCheck size={20} /> : <IconClose size={18} />}<span className="sr-only">{i === 0 ? 'ja' : 'nein'}</span></span>
          <span role="cell" className="is-yes"><IconCheck size={20} /><span className="sr-only">ja</span></span>
        </div>
      ))}
    </div>
  );
}

function Table({ rows }: { rows: string[][] }) {
  const [head, ...body] = rows;
  return (
    <div className="rich__table-wrap">
      <table className="rich__table">
        <thead><tr>{head.map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
        <tbody>{body.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}>{c}</td>)}</tr>)}</tbody>
      </table>
    </div>
  );
}

/** Listenpunkte „Titel: Text“ mit hervorgehobenem Titel */
function Item({ text }: { text: string }) {
  const t = clean(text);
  const m = t.match(/^([^:]{3,60}):\s+(.+)$/);
  return m ? <><strong>{m[1]}:</strong> {m[2]}</> : <>{t}</>;
}

function Block({ b }: { b: RichBlock }) {
  switch (b.t) {
    case 'h1': return <h2 className="rich__h2 head">{clean(b.text)}</h2>;
    case 'h2': return <h2 className="rich__h2 head">{clean(b.text)}</h2>;
    case 'h3': return <h3 className="rich__h3 head">{clean(b.text)}</h3>;
    case 'h4': return <h4 className="rich__h4">{clean(b.text)}</h4>;
    case 'p': return <p className="rich__p">{clean(b.text)}</p>;
    case 'blockquote': return <blockquote className="rich__quote head">{clean(b.text)}</blockquote>;
    case 'ul': return <ul className="rich__checks">{b.items.map((x, i) => <li key={i}><span className="rich__tick"><IconCheck size={14} /></span><span><Item text={x} /></span></li>)}</ul>;
    case 'ol': return <ol className="rich__ol">{b.items.map((x, i) => <li key={i}><Item text={x} /></li>)}</ol>;
    case 'table': return b.rows[0]?.some((c) => /KLASSISCHER MAKLER/i.test(c)) ? <Compare rows={b.rows} /> : <Table rows={b.rows} />;
    case 'img': return <figure className="rich__fig"><img src={b.src} alt={b.alt} loading="lazy" /></figure>;
    case 'pdf': return <a className="btn btn--outline btn--small" href={b.href} download>PDF herunterladen</a>;
    default: return null;
  }
}

export function TeamStrip({ imgs }: { imgs: { src: string; alt: string }[] }) {
  return (
    <ul className="rich__team">
      {imgs.map((m) => {
        const p = personOf(m.alt);
        return <li key={m.src}><span className="rich__team-img"><img src={m.src} alt="" loading="lazy" /></span><strong>{p.name}</strong><span>{p.role}</span></li>;
      })}
    </ul>
  );
}

export function AdvisorCard({ img, title = 'Ihr Ansprechpartner' }: { img: { src: string; alt: string }; title?: string }) {
  const p = personOf(img.alt);
  return (
    <aside className="rich__advisor">
      <span className="rich__advisor-img"><img src={faceOf(p.name) ?? img.src} alt="" loading="lazy" /></span>
      <div>
        <p className="eyebrow">{title}</p>
        <p className="rich__advisor-name head">{p.name}</p>
        {p.role && <p className="rich__advisor-role">{p.role}</p>}
        <p className="rich__advisor-links"><a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a> · <Link to={ROUTES.kontakt} className="link-underline">Nachricht schreiben</Link></p>
      </div>
    </aside>
  );
}

export function Faces() {
  return (
    <button type="button" className="rich__faces rating-trigger" onClick={openRatings} aria-haspopup="dialog">
      <span className="rich__faces-imgs">{reviewFaces.map((f) => <img key={f} src={f} alt="" loading="lazy" />)}</span>
      <span><Stars value={brand.rating} /> <strong>{brand.rating.toFixed(1).replace('.', ',')}/5</strong> aus {brand.reviews} Google-Bewertungen</span>
    </button>
  );
}

export function FaqBlock({ title, items, eyebrow = 'FAQ' }: { title: string; items: QA[]; eyebrow?: string }) {
  if (!items.length) return null;
  return (
    <section className="rich__faq">
      <p className="eyebrow">{eyebrow}</p>
      <h2 className="rich__h2 head">{title}</h2>
      <Accordion items={items.map((x) => ({ title: clean(x.q), content: <p>{clean(x.a)}</p> }))} />
    </section>
  );
}

/** Rendert Inhaltsblöcke. `skip` entfernt bereits im Seitenkopf verwendete Blöcke. */
export default function Rich({ blocks, faq = [], after }: { blocks: RichBlock[]; faq?: QA[]; after?: ReactNode }) {
  const nodes = parse(blocks, faq);
  return (
    <div className="rich">
      {nodes.map((n, i) => {
        switch (n.k) {
          case 'block': return <div key={i} className="rich__text"><Block b={n.b} /></div>;
          case 'eyebrow': return <div key={i} className="rich__text"><p className="eyebrow rich__eyebrow">{n.text}</p></div>;
          case 'team': return <div key={i} className="rich__wide"><TeamStrip imgs={n.imgs} /></div>;
          case 'advisor': return <div key={i} className="rich__text"><AdvisorCard img={n.img} /></div>;
          case 'faces': return <div key={i} className="rich__text"><Faces /></div>;
          case 'columns': return (
            <div key={i} className="rich__wide">
              <div className={`rich__cols rich__cols--${Math.min(n.items.length, 3)}`}>
                {n.items.map((c) => (
                  <section key={c.title} className="rich__col">
                    <h3 className="head">{clean(c.title)}</h3>
                    <ul className="rich__checks">{c.items.map((x) => <li key={x}><span className="rich__tick"><IconCheck size={14} /></span><span>{clean(x)}</span></li>)}</ul>
                  </section>
                ))}
              </div>
            </div>
          );
          case 'steps': return (
            <div key={i} className="rich__wide">
              <h2 className="rich__h2 rich__h2--center head">{clean(n.title)}</h2>
              <ol className={`rich__steps rich__steps--${Math.min(n.items.length, 4)}`}>
                {n.items.map((s, k) => <li key={s.title}><span className="rich__step-no">Schritt {k + 1}</span><h3 className="head">{clean(s.title)}</h3><p>{clean(s.text)}</p></li>)}
              </ol>
            </div>
          );
          case 'faq': return <div key={i} className="rich__text"><FaqBlock title={n.title} items={n.items} /></div>;
          case 'brochure': return (
            <div key={i} className="rich__text">
              <a className="rich__brochure" href={n.href} download>
                <span className="rich__brochure-imgs">{n.images.map((s) => <img key={s} src={s} alt="" loading="lazy" />)}</span>
                <span><span className="eyebrow">Broschüre (PDF)</span><span className="rich__brochure-title head">Vermittlung mit Energiekompetenz</span><span className="rich__brochure-cta">Jetzt herunterladen <IconArrowRight size={18} /></span></span>
              </a>
            </div>
          );
          default: return <Fragment key={i} />;
        }
      })}
      {after}
    </div>
  );
}
