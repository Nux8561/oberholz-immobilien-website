import { useEffect, useRef, useState } from 'react';
import { brand } from '../../data/content';
import Stars from '../Stars/Stars';
import { IconChevronDown, IconClose } from '../Icons';
import './RatingPanel.css';

const EVT = 'oh-rating-open';
export const openRatings = () => window.dispatchEvent(new Event(EVT));

const SCALE: [string, string][] = [['5,00 – 4,50', 'Sehr gut'], ['4,49 – 3,50', 'Gut'], ['3,49 – 2,50', 'Befriedigend'], ['2,49 – 1,50', 'Ausreichend'], ['1,49 – 1,00', 'Mangelhaft']];
const grade = (v: number) => (v >= 4.5 ? 'Sehr gut' : v >= 3.5 ? 'Gut' : v >= 2.5 ? 'Befriedigend' : v >= 1.5 ? 'Ausreichend' : 'Mangelhaft');

/** Bewertungs-Panel wie auf der bisherigen Website: Klick auf die Bewertung öffnet die Übersicht,
 *  ein zweiter Klick führt zum Google-Unternehmensprofil mit allen Rezensionen. */
export default function RatingPanel() {
  const [open, setOpen] = useState(false);
  const [origin, setOrigin] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const show = () => setOpen(true);
    window.addEventListener(EVT, show);
    const onHash = () => { if (window.location.hash === '#bewertungen') { setOpen(true); history.replaceState(null, '', window.location.pathname + window.location.search); } };
    onHash();
    window.addEventListener('hashchange', onHash);
    return () => { window.removeEventListener(EVT, show); window.removeEventListener('hashchange', onHash); };
  }, []);
  useEffect(() => {
    if (!open) return;
    document.body.classList.add('no-scroll');
    ref.current?.querySelector<HTMLElement>('button')?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', onKey);
    return () => { document.body.classList.remove('no-scroll'); document.removeEventListener('keydown', onKey); };
  }, [open]);

  return (
    <div className={`rpanel${open ? ' is-open' : ''}`} aria-hidden={!open}>
      <button type="button" className="rpanel__backdrop" aria-label="Schließen" tabIndex={-1} onClick={() => setOpen(false)} />
      <aside className="rpanel__sheet" role="dialog" aria-modal="true" aria-labelledby="rpanel-title" ref={ref}>
        <div className="rpanel__head">
          <p className="head" id="rpanel-title">Echte Bewertungen für {brand.name}</p>
          <button type="button" aria-label="Schließen" onClick={() => setOpen(false)}><IconClose /></button>
        </div>
        <div className="rpanel__score">
          <svg width="48" height="48" viewBox="0 0 48 48" aria-hidden="true"><path fill="#4285F4" d="M44.5 24.5c0-1.6-.1-2.8-.4-4H24v7.6h11.7c-.3 2-1.6 4.9-4.6 6.9l7 5.4c4.2-3.9 6.4-9.6 6.4-15.9Z" /><path fill="#34A853" d="M24 45c5.8 0 10.6-1.9 14.1-5.2l-7-5.4c-1.9 1.3-4.4 2.2-7.1 2.2-5.4 0-10-3.6-11.6-8.5l-7.2 5.6C8.7 40.6 15.8 45 24 45Z" /><path fill="#FBBC05" d="M12.4 28.1c-.4-1.3-.7-2.6-.7-4.1s.3-2.8.7-4.1l-7.2-5.6A21 21 0 0 0 3 24c0 3.4.8 6.6 2.2 9.7l7.2-5.6Z" /><path fill="#EA4335" d="M24 11.4c4 0 6.7 1.7 8.2 3.2l6-5.9C34.6 5.3 29.8 3 24 3 15.8 3 8.7 7.4 5.2 14.3l7.2 5.6c1.6-4.9 6.2-8.5 11.6-8.5Z" /></svg>
          <Stars value={brand.rating} />
          <p className="rpanel__value head">{brand.rating.toFixed(1).replace('.', ',')} <small>/ 5</small></p>
          <p className="rpanel__grade">{grade(brand.rating).toUpperCase()}</p>
          <p className="rpanel__count">Basierend auf {brand.reviews} Google-Bewertungen</p>
        </div>
        <table className="rpanel__scale">
          <caption>Notenberechnung basierend auf Sternen</caption>
          <tbody>{SCALE.map(([r, g]) => <tr key={g} className={g === grade(brand.rating) ? 'is-active' : ''}><td>{r}</td><td>{g}</td></tr>)}</tbody>
        </table>
        <button type="button" className="rpanel__origin-btn" aria-expanded={origin} onClick={() => setOrigin(!origin)}>
          Woher stammen diese Bewertungen? <IconChevronDown size={16} />
        </button>
        {origin && (
          <div className="rpanel__origin">
            <p>Die angezeigten Bewertungen stammen aus dem öffentlichen Google-Unternehmensprofil von {brand.name} ({brand.street}, {brand.city.replace(', Deutschland', '')}).</p>
            <p>Es handelt sich um echte Google-Kundenrezensionen – unverändert und öffentlich nachvollziehbar.</p>
          </div>
        )}
        <a className="btn btn--accent rpanel__cta" href={brand.googleUrl} target="_blank" rel="noopener noreferrer">Alle Google-Bewertungen ansehen</a>
        <a className="link-underline rpanel__write" href={brand.googleUrl} target="_blank" rel="noopener noreferrer">Selbst eine Bewertung schreiben</a>
      </aside>
    </div>
  );
}
