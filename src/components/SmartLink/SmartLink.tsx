import { useEffect, type ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { routeFor } from '../../data/routes';
import { openCookieSettings } from '../Cookies/Cookies';
import { openRatings } from '../RatingPanel/RatingPanel';
import { notify } from '../Toast/Toast';

type Props = {
  label: string;
  /** feste Route, externe URL oder „#cookies“; ohne Angabe wird sie über routeFor(label) ermittelt */
  to?: string | null;
  className?: string;
  children?: ReactNode;
  onNavigate?: () => void;
  tabIndex?: number;
  'aria-label'?: string;
};

export const isExternal = (to: string) => /^(https?:|mailto:|tel:)/.test(to);

/** Einheitlicher Link: interne Routen, externe Ziele (neuer Tab) und die Cookie-Einstellungen. */
export default function SmartLink({ label, to, className, children, onNavigate, tabIndex, ...rest }: Props) {
  const target = to === undefined ? routeFor(label) : to;
  const common = { className, tabIndex, 'aria-label': rest['aria-label'] };
  if (target === '#cookies') {
    return <a href="#cookies" {...common} onClick={(e) => { e.preventDefault(); onNavigate?.(); openCookieSettings(); }}>{children ?? label}</a>;
  }
  if (target === '#bewertungen') {
    return <a href="#bewertungen" {...common} onClick={(e) => { e.preventDefault(); onNavigate?.(); openRatings(); }}>{children ?? label}</a>;
  }
  if (target && isExternal(target)) {
    const blank = target.startsWith('http');
    return <a href={target} {...common} {...(blank ? { target: '_blank', rel: 'noopener noreferrer' } : {})} onClick={() => onNavigate?.()}>{children ?? label}</a>;
  }
  if (target) {
    return <Link to={target} {...common} onClick={() => onNavigate?.()}>{children ?? label}</Link>;
  }
  // Sollte nicht vorkommen – die Link-Prüfung (scripts/check_links.py) meldet solche Fälle.
  return (
    <a href="#" {...common} data-missing-route="true"
      onClick={(e) => { e.preventDefault(); onNavigate?.(); notify(`„${label}“ ist noch nicht verknüpft.`); }}>
      {children ?? label}
    </a>
  );
}

/** Scrollt bei Routenwechsel nach oben bzw. zum Anker (#team). */
export function ScrollManager() {
  const { pathname, hash, search } = useLocation();
  useEffect(() => {
    if (hash && hash !== '#cookies' && hash !== '#bewertungen') {
      // Ziel kann in einer nachgeladenen Seite liegen → bis zu 2 s nach dem Element suchen
      const id = decodeURIComponent(hash.slice(1));
      let tries = 0;
      const t = window.setInterval(() => {
        const el = document.getElementById(id);
        if (el || ++tries > 25) { window.clearInterval(t); el?.scrollIntoView({ block: 'start' }); }
      }, 80);
      return () => window.clearInterval(t);
    }
    window.scrollTo(0, 0);
  }, [pathname, hash, search]);
  return null;
}
