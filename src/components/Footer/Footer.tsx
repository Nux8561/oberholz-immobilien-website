import { useState } from 'react';
import { brand, footer, partners, whatsappUrl } from '../../data/content';
import { FooterIllustration, IconChevronUp, IconMinus, IconPlus, SocialIcon } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import './Footer.css';

/** variant 'open': Linkspalten offen (Startseite); 'accordion': auch Desktop zugeklappt mit + (Unterseiten) */
export default function Footer({ variant = 'open' }: { variant?: 'open' | 'accordion' }) {
  const [open, setOpen] = useState<number | null>(null);
  const socialUrl = { linkedin: brand.linkedinUrl, google: brand.googleUrl, whatsapp: whatsappUrl() } as const;
  const socialLabel = { linkedin: 'LinkedIn', google: 'Google-Bewertungen', whatsapp: 'WhatsApp' } as const;

  return (
    <footer className={`ftr ftr--${variant}`}>
      <div className="ftr__wrap">
        <div className="ftr__contacts">
          <p className="ftr__title head">{footer.title}</p>
          <p className="ftr__address">{brand.street}, {brand.city}</p>
          <p className="ftr__phone"><a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a><br /><a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a></p>
          <ul className="ftr__social-list">
            {footer.socials.map((s) => (
              <li key={s}><a href={socialUrl[s]} className="ftr__social-link" target="_blank" rel="noopener noreferrer" aria-label={socialLabel[s]}><SocialIcon name={s} /></a></li>
            ))}
          </ul>
          <button type="button" className="ftr__top" aria-label="nach oben" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <IconChevronUp />
          </button>
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

      <div className="ftr__wrap">
        <div className="ftr__partners">
          <p className="ftr__col-title">In Kooperation mit</p>
          <ul>
            {partners.kooperation.map((p) => (
              <li key={p.name}><a href={p.url} target="_blank" rel="noopener noreferrer" title={p.name}><img src={p.logo} alt={p.name} loading="lazy" /></a></li>
            ))}
          </ul>
        </div>
      </div>

      <div className="ftr__wrap ftr__wrap--bottom">
        <div className="ftr__bottom">
          <ul className="ftr__legal">
            {footer.legalLeft.map((l) => <li key={l.label}><SmartLink label={l.label} to={l.to} className="ftr__link" /></li>)}
          </ul>
          <FooterIllustration className="ftr__illu" />
          <ul className="ftr__legal ftr__legal--right">
            {footer.legalRight.map((l) => <li key={l.label}><SmartLink label={l.label} to={l.to} className="ftr__link" /></li>)}
            <li><span className="ftr__copy">© {new Date().getFullYear()} {brand.name}</span></li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
