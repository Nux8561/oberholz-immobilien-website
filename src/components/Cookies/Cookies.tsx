import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import { IconClose } from '../Icons';
import { notify } from '../Toast/Toast';
import './Cookies.css';

const EVT = 'oh-cookie-settings';
export const openCookieSettings = () => window.dispatchEvent(new Event(EVT));

const KEY = 'oh-cookie-komfort';
export const comfortAllowed = () => {
  try { return window.localStorage.getItem(KEY) !== '0'; } catch { return true; }
};

/** Cookie-Einstellungen: Die Website setzt keine Tracking- oder Marketing-Cookies.
 *  Einstellbar ist nur die lokale Speicherung von Merkliste und Suchaufträgen. */
export default function CookieSettings() {
  const [open, setOpen] = useState(false);
  const [comfort, setComfort] = useState(true);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const show = () => { setComfort(comfortAllowed()); setOpen(true); };
    window.addEventListener(EVT, show);
    return () => window.removeEventListener(EVT, show);
  }, []);
  useEffect(() => {
    if (!open) return;
    ref.current?.querySelector<HTMLElement>('button')?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open]);

  if (!open) return null;
  const save = () => {
    try {
      window.localStorage.setItem(KEY, comfort ? '1' : '0');
      if (!comfort) { window.localStorage.removeItem('oh-favoriten'); window.localStorage.removeItem('oh-suchen'); }
    } catch { /* Speicher nicht verfügbar */ }
    setOpen(false);
    notify('Ihre Cookie-Einstellungen wurden gespeichert.');
  };

  return (
    <div className="cookies" role="dialog" aria-modal="true" aria-labelledby="cookies-title" ref={ref}>
      <button type="button" className="cookies__backdrop" aria-label="Schließen" onClick={() => setOpen(false)} />
      <div className="cookies__panel">
        <div className="cookies__head">
          <p className="head" id="cookies-title">Cookie-Einstellungen</p>
          <button type="button" aria-label="Schließen" onClick={() => setOpen(false)}><IconClose /></button>
        </div>
        <p>Wir verwenden keine Tracking-, Analyse- oder Marketing-Cookies. Schriften und Bilder werden von unserem eigenen Server geladen.</p>
        <ul className="cookies__list">
          <li>
            <div><p className="cookies__name">Technisch notwendig</p><p>Darstellung der Seite, Sicherheit und Ihre Auswahl in diesem Dialog.</p></div>
            <span className="cookies__always">Immer aktiv</span>
          </li>
          <li>
            <div><p className="cookies__name">Komfortfunktionen</p><p>Merkliste und gespeicherte Suchen werden ausschließlich in Ihrem Browser gespeichert.</p></div>
            <label className="cookies__switch">
              <input type="checkbox" checked={comfort} onChange={(e) => setComfort(e.target.checked)} />
              <span className="switch" aria-hidden="true"><span /></span>
              <span className="sr-only">Komfortfunktionen erlauben</span>
            </label>
          </li>
        </ul>
        <p className="cookies__more">Details in den <Link to={ROUTES.cookieHinweise} onClick={() => setOpen(false)} className="link-underline">Cookie-Hinweisen</Link> und der <Link to={ROUTES.datenschutz} onClick={() => setOpen(false)} className="link-underline">Datenschutzerklärung</Link>.</p>
        <div className="cookies__btns">
          <button type="button" className="btn btn--outline btn--small" onClick={() => { setComfort(false); }}>Nur notwendige</button>
          <button type="button" className="btn btn--small" onClick={save}>Auswahl speichern</button>
        </div>
      </div>
    </div>
  );
}
