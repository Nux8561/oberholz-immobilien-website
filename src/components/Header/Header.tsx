import { useCallback, useEffect, useRef, useState } from 'react';
import Logo from '../Logo';
import MegaMenu from '../MegaMenu/MegaMenu';
import MobileMenu from '../MegaMenu/MobileMenu';
import { megaMenus } from '../../data/content';
import { IconMenu, IconPin, IconUser } from '../Icons';
import { useFavorites } from '../../lib/store';
import { brand } from '../../data/content';
import { openRatings } from '../RatingPanel/RatingPanel';
import SmartLink from '../SmartLink/SmartLink';
import { useLocation } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import './Header.css';

const OPEN_DELAY = 120;
const CLOSE_DELAY = 180;

export default function Header() {
  const [open, setOpen] = useState<number | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const openTimer = useRef<number>();
  const closeTimer = useRef<number>();
  const headerRef = useRef<HTMLElement>(null);
  const { pathname } = useLocation();

  const clearTimers = () => {
    window.clearTimeout(openTimer.current);
    window.clearTimeout(closeTimer.current);
  };
  const scheduleOpen = (i: number) => {
    clearTimers();
    openTimer.current = window.setTimeout(() => setOpen(i), open === null ? OPEN_DELAY : 0);
  };
  const scheduleClose = () => {
    clearTimers();
    closeTimer.current = window.setTimeout(() => setOpen(null), CLOSE_DELAY);
  };
  const close = useCallback(() => { clearTimers(); setOpen(null); }, []);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 0);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    const onDown = (e: MouseEvent) => {
      if (headerRef.current && !headerRef.current.contains(e.target as Node)) close();
    };
    document.addEventListener('keydown', onKey);
    document.addEventListener('mousedown', onDown);
    return () => { document.removeEventListener('keydown', onKey); document.removeEventListener('mousedown', onDown); };
  }, [close]);

  // Menüs bei Seitenwechsel schließen
  useEffect(() => { close(); setMobileOpen(false); }, [pathname, close]);

  const fav = useFavorites();

  return (
    <header className={`hdr${scrolled ? ' is-scrolled' : ''}`} ref={headerRef} onMouseLeave={scheduleClose} onMouseEnter={() => window.clearTimeout(closeTimer.current)}>
      <div className="hdr__top">
        <button type="button" className="hdr__burger" aria-label="Navigation öffnen" aria-expanded={mobileOpen} onClick={() => setMobileOpen(true)}>
          <IconMenu />
        </button>
        <div className="hdr__logo"><Logo /></div>
        <ul className="hdr__meta">
          <li className="hdr__meta-desk">
            <button type="button" className="hdr__meta-item hdr__rating" onClick={openRatings} aria-haspopup="dialog" aria-label={`Google-Bewertung ${brand.rating.toFixed(1).replace('.', ',')} von 5 – Bewertungen ansehen`}>
              <span className="hdr__rating-star" aria-hidden="true">★</span>
              <span className="hdr__meta-label"><strong>{brand.rating.toFixed(1).replace('.', ',')}</strong>/5 · {brand.reviews} Google-Bewertungen</span>
            </button>
          </li>
          <li>
            <SmartLink label="Mein Bereich" to={ROUTES.meinBereich} className="hdr__meta-item" aria-label={`Mein Bereich${fav.ids.length ? ` (${fav.ids.length} gemerkt)` : ''}`}>
              <IconUser /><span className="hdr__meta-label">Mein Bereich</span>
              {fav.ids.length > 0 && <span className="hdr__badge" aria-hidden="true">{fav.ids.length}</span>}
            </SmartLink>
          </li>
          <li className="hdr__meta-desk">
            <SmartLink label="Regionen" to={ROUTES.regionen} className="hdr__meta-item">
              <IconPin /><span className="hdr__meta-label">Regionen</span>
            </SmartLink>
          </li>
        </ul>
      </div>

      <div className="hdr__bottom">
        <nav className="hdr__nav" aria-label="Hauptnavigation">
          <ul className="hdr__list">
            {megaMenus.map((m, i) => (
              <li key={m.label} className="hdr__item" onMouseEnter={() => scheduleOpen(i)}>
                <SmartLink label={m.label} to={m.to} className={`hdr__link${open === i ? ' is-active' : ''}`} onNavigate={close}>
                  {m.label}
                </SmartLink>
                <button type="button" className="hdr__flyout-trigger" aria-expanded={open === i} aria-controls={`flyout-${i}`}
                  onClick={() => (open === i ? close() : (clearTimers(), setOpen(i)))}>
                  <span className="sr-only">{m.label} Untermenü öffnen</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>
        <div className="hdr__cta">
          <SmartLink label="Jetzt kontaktieren" to={ROUTES.kontakt} className="btn btn--small" />
        </div>
      </div>

      <MegaMenu openIndex={open} onClose={close} />
      <MobileMenu open={mobileOpen} onClose={() => setMobileOpen(false)} />
    </header>
  );
}
