import { useState } from 'react';
import { Link } from 'react-router-dom';
import { attributes, formatPrice, type Property } from '../../data/properties';
import { ROUTES } from '../../data/routes';
import { IconChevronLeft, IconChevronRight } from '../Icons';
import { useFavorites } from '../../lib/store';
import FitImage from '../FitImage/FitImage';
import { notify } from '../Toast/Toast';
import './PropertyCard.css';

const IconHeart = ({ filled }: { filled: boolean }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M12 20.3 4.6 13a4.6 4.6 0 0 1 6.5-6.6l.9.9.9-.9A4.6 4.6 0 0 1 19.4 13Z" fill={filled ? 'var(--c-accent)' : 'rgba(13,13,13,.6)'} stroke="#fff" strokeWidth="1.4" />
  </svg>
);

/** Objektkarte – Referenz (Suchliste 1440): 437px breit, Bild 437×292 mit Mini-Slider, Body 16px Padding. */
export default function PropertyCard({ p, compact = false }: { p: Property; compact?: boolean }) {
  const [img, setImg] = useState(0);
  const favs = useFavorites();
  const fav = favs.has(p.id);
  const step = (d: number) => (e: React.MouseEvent) => { e.preventDefault(); setImg((i) => (i + d + p.images.length) % p.images.length); };

  return (
    <article className={`pcard${compact ? ' pcard--compact' : ''}`}>
      <Link to={ROUTES.expose(p.id)} className="pcard__link" aria-label={p.title} />
      <div className="pcard__media">
        <div className="pcard__track" style={{ transform: `translateX(${-img * 100}%)` }}>
          {p.images.map((src, i) => <FitImage key={i} src={src} alt={i === 0 ? p.title : ''} className="pcard__slide" />)}
        </div>
        {p.badges.length > 0 && (
          <div className="pcard__badges">{p.badges.map((b) => <span key={b} className={`pcard__badge${b === 'Exklusiv' ? ' pcard__badge--dark' : ''}`}>{b}</span>)}</div>
        )}
        <button type="button" className={`pcard__fav${fav ? ' is-active' : ''}`} aria-pressed={fav} aria-label={fav ? 'Von Favoriten entfernen' : 'Zu Favoriten hinzufügen'}
          onClick={(e) => { e.preventDefault(); notify(favs.toggle(p.id) ? 'Zur Merkliste hinzugefügt – zu finden unter „Mein Bereich“.' : 'Von der Merkliste entfernt.'); }}>
          <IconHeart filled={fav} />
        </button>
        {p.images.length > 1 && (
          <>
            <button type="button" className="pcard__nav pcard__nav--prev" aria-label="Vorheriges Bild" onClick={step(-1)}><IconChevronLeft size={20} /></button>
            <button type="button" className="pcard__nav pcard__nav--next" aria-label="Nächstes Bild" onClick={step(1)}><IconChevronRight size={20} /></button>
            <div className="pcard__dots" aria-hidden="true">
              {p.images.slice(0, 4).map((_, i) => <span key={i} className={i === img ? 'is-active' : ''} />)}
            </div>
          </>
        )}
      </div>
      <div className="pcard__body">
        <p className="pcard__loc">{p.zip} {p.city}{p.district ? `, ${p.district}` : ''}</p>
        <h2 className="pcard__title head">{p.title}</h2>
        {p.price === null ? (
          <p className="pcard__price pcard__price--request">Preis auf Anfrage</p>
        ) : (
          <>
            <p className="pcard__label">{p.priceLabel}</p>
            <p className="pcard__price">{formatPrice(p)}</p>
          </>
        )}
        <ul className="pcard__attrs">{attributes(p).map((a) => <li key={a}>{a}</li>)}</ul>
        {p.provision && !compact && <p className="pcard__prov">{p.provision}</p>}
      </div>
    </article>
  );
}
