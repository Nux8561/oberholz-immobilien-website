import { useEffect, useRef, useState } from 'react';
import { megaMenus } from '../../data/content';
import Logo from '../Logo';
import { IconChevronLeft, IconChevronRight, IconClose, IconPin, IconUser } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import { ROUTES } from '../../data/routes';
import './MobileMenu.css';

/** Mobile-/Tablet-Navigation: Vollbild-Panel, Untermenüs schieben von rechts herein (Referenz 390px). */
export default function MobileMenu({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [sub, setSub] = useState<number | null>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.body.classList.toggle('no-scroll', open);
    if (!open) { setSub(null); return; }
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    panelRef.current?.querySelector<HTMLElement>('button')?.focus();
    return () => document.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  const m = sub !== null ? megaMenus[sub] : null;

  return (
    <div className={`mnav${open ? ' is-open' : ''}`} role="dialog" aria-modal="true" aria-label="Navigation" aria-hidden={!open} ref={panelRef}>
      <div className={`mnav__track${sub !== null ? ' is-sub' : ''}`}>
        <section className="mnav__panel" aria-hidden={sub !== null}>
          <div className="mnav__bar">
            <button type="button" className="mnav__icon" aria-label="Navigation schließen" onClick={onClose}><IconClose /></button>
            <Logo compact />
            <SmartLink label="Mein Bereich" to={ROUTES.meinBereich} className="mnav__icon" aria-label="Mein Bereich" onNavigate={onClose}><IconUser /></SmartLink>
          </div>
          <ul className="mnav__list">
            {megaMenus.map((item, i) => (
              <li key={item.label}>
                <button type="button" className="mnav__row head" onClick={() => setSub(i)}>
                  {item.label}<IconChevronRight />
                </button>
              </li>
            ))}
          </ul>
          <ul className="mnav__meta">
            <li><SmartLink label="Regionen" to={ROUTES.regionen} className="mnav__meta-item" onNavigate={onClose}><IconPin />Regionen</SmartLink></li>
            <li><SmartLink label="Mein Bereich" to={ROUTES.meinBereich} className="mnav__meta-item" onNavigate={onClose}><IconUser />Mein Bereich</SmartLink></li>
          </ul>
          <SmartLink label="Jetzt kontaktieren" to={ROUTES.kontakt} className="btn btn--small mnav__cta" onNavigate={onClose} />
        </section>

        <section className="mnav__panel mnav__panel--sub" aria-hidden={sub === null}>
          <div className="mnav__bar">
            <button type="button" className="mnav__icon" aria-label="Zurück zum Hauptmenü" onClick={() => setSub(null)}><IconChevronLeft /></button>
            <span className="mnav__bar-title">Hauptmenü</span>
            <button type="button" className="mnav__icon" aria-label="Navigation schließen" onClick={onClose}><IconClose /></button>
          </div>
          {m && (
            <div className="mnav__sub">
              <SmartLink label={m.title} to={m.to} className="mnav__sub-title head" onNavigate={onClose} />
              {m.columns.map((c) => (
                <div key={c.eyebrow} className="mnav__sub-col">
                  <p className="eyebrow">{c.eyebrow}</p>
                  <ul>
                    {c.links.map((l) => (<li key={l.label}><SmartLink label={l.label} to={l.to} className="mnav__sub-link" onNavigate={onClose} /></li>))}
                  </ul>
                </div>
              ))}
              <SmartLink label={m.mobileCta.label} to={m.mobileCta.to} className="btn btn--outline mnav__sub-cta" onNavigate={onClose} />
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
