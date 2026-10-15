import { megaMenus } from '../../data/content';
import { IconArrowRight } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import './MegaMenu.css';

/** Desktop-Flyouts: volle Breite unter der Navigation, 4-Spalten-Raster (Referenz 1360px, Gap 24px). */
export default function MegaMenu({ openIndex, onClose }: { openIndex: number | null; onClose: () => void }) {
  return (
    <>
      {megaMenus.map((m, i) => (
        <div key={m.label} id={`flyout-${i}`} className={`flyout${openIndex === i ? ' is-open' : ''}`} aria-hidden={openIndex !== i}>
          <div className={`flyout__inner${m.promo.stacked ? ' flyout__inner--wide' : ''}`}>
            <div className="flyout__intro">
              <p className="flyout__title head">{m.title}</p>
              <p className="flyout__text">{m.text}</p>
            </div>
            {m.columns.map((c) => (
              <div className="flyout__col" key={c.eyebrow}>
                <p className="eyebrow flyout__eyebrow">{c.eyebrow}</p>
                <ul>
                  {c.links.map((l) => (
                    <li key={l.label}><SmartLink label={l.label} to={l.to} className="flyout__link" tabIndex={openIndex === i ? 0 : -1} onNavigate={onClose} /></li>
                  ))}
                </ul>
              </div>
            ))}
            <SmartLink label={m.promo.title} to={m.promo.to} className={`promo${m.promo.stacked ? ' promo--stacked' : ''}`} tabIndex={openIndex === i ? 0 : -1} onNavigate={onClose}>
              <span className="promo__media"><img src={m.promo.image} alt="" loading="lazy" /></span>
              <span className="promo__body">
                <span className="eyebrow promo__eyebrow">{m.promo.eyebrow}</span>
                <span className="promo__title head">{m.promo.title}</span>
                <IconArrowRight className="promo__arrow" />
              </span>
            </SmartLink>
          </div>
        </div>
      ))}
    </>
  );
}
