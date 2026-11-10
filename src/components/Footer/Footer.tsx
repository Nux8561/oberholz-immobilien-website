import { useState } from 'react';
import { Link } from 'react-router-dom';
import { brand, footer, officeLink, offices, whatsappUrl } from '../../data/content';
import { IconChevronUp, IconMinus, IconPlus, SocialIcon } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import './Footer.css';

/** variant 'open': Linkspalten offen (Startseite); 'accordion': zugeklappt mit + (Unterseiten) */
export default function Footer({ variant = 'open' }: { variant?: 'open' | 'accordion' }) {
  const [open, setOpen] = useState<number | null>(null);
  const socialUrl = { google: brand.googleUrl, whatsapp: whatsappUrl() } as const;
  const socialLabel = { google: 'Google-Bewertungen', whatsapp: 'WhatsApp' } as const;

  return (
    <footer className={`ftr ftr--${variant}`}>
      <div className="ftr__wrap ftr__wrap--brand">
        <div className="ftr__brand">
          <Link to="/" className="ftr__logo" aria-label={`${brand.name}, Startseite`}>
            <img src={brand.logo} alt={brand.name} width={200} height={92} />
          </Link>
          <div className="ftr__brand-copy">
            <p className="ftr__claim head">{footer.claim}</p>
            <p className="ftr__tagline">{brand.claim}</p>
            <p className="ftr__reach">
              Essen: <a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a>
              <br />
              Münster: <a href={brand.phoneMuensterHref} className="link-underline">{brand.phoneMuensterDisplay}</a>
              <br />
              WhatsApp: <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer" className="link-underline">{brand.whatsappDisplay}</a>
              <br />
              <a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a>
            </p>
            <ul className="ftr__social-list">
              {footer.socials.map((s) => (
                <li key={s}>
                  <a href={socialUrl[s]} className="ftr__social-link" target="_blank" rel="noopener noreferrer" aria-label={socialLabel[s]}>
                    <SocialIcon name={s} />
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <button type="button" className="ftr__top" aria-label="nach oben" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <IconChevronUp />
          </button>
        </div>
      </div>

      <div className="ftr__wrap">
        <div className="ftr__offices">
          {offices.map((o) => (
            <div key={o.slug} className={`ftr__office${o.hub ? ' is-hub' : ''}`}>
              <p className="ftr__office-city">{o.city}</p>
              <p className="ftr__office-addr">{o.street}<br />{o.zipCity}</p>
              <p className="ftr__office-phone"><a href={o.phoneHref} className="link-underline">{o.phoneDisplay}</a></p>
              <Link to={officeLink(o)} className="ftr__office-link link-underline">Region ansehen</Link>
            </div>
          ))}
        </div>
      </div>

      <div className="ftr__wrap ftr__wrap--links">
        <div className="ftr__cols">
          {footer.columns.map((c, i) => (
            <div key={c.title} className={`ftr__col${open === i ? ' is-open' : ''}`}>
              <p className="ftr__col-title">{c.title}</p>
              <button type="button" className="ftr__acc" aria-expanded={open === i} aria-controls={`ftr-col-${i}`} onClick={() => setOpen(open === i ? null : i)}>
                <span>{c.title}</span>{open === i ? <IconMinus /> : <IconPlus />}
              </button>
              <ul className="ftr__list" id={`ftr-col-${i}`}>
                {c.links.map((l) => <li key={l.label}><SmartLink label={l.label} to={l.to} className="ftr__link" /></li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="ftr__wrap ftr__wrap--bottom">
        <div className="ftr__bottom">
          <ul className="ftr__legal">
            {footer.legalLeft.map((l) => <li key={l.label}><SmartLink label={l.label} to={l.to} className="ftr__link" /></li>)}
          </ul>
          <ul className="ftr__legal ftr__legal--right">
            {footer.legalRight.map((l) => <li key={l.label}><SmartLink label={l.label} to={l.to} className="ftr__link" /></li>)}
            <li><span className="ftr__copy">© {new Date().getFullYear()} {brand.name}</span></li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
