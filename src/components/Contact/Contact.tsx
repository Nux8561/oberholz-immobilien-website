import { brand, contact, whatsappUrl } from '../../data/content';
import SectionIntro from '../SectionIntro/SectionIntro';
import { IconMail } from '../Icons';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import Deco from '../Deco/Deco';
import './Contact.css';

export default function Contact({ variant = 'home' }: { variant?: 'home' | 'page' }) {
  return (
    <section className={`contact contact--${variant}`} id="kontakt" aria-labelledby="kontakt-title">
      <div className="contact__inner">
        <div className="wrap contact__wrap">
          <SectionIntro variant="inline" line={false} center eyebrow={contact.eyebrow} title={contact.title} id="kontakt-title" />
          <div className="contact__avatars">
            {contact.avatars.map((a, i) => <img key={a} src={a} alt={i === 0 ? 'Michael Oberholz' : 'Felix Lesch'} width={56} height={56} />)}
          </div>
          <span className="contact__line" aria-hidden="true" />
          <address className="contact__address">
            <p className="contact__office head">{contact.office}</p>
            <p>{brand.street}</p>
            <p>{brand.city}</p>
            <p>Tel: <a href={brand.phoneHref} className="link-underline">{brand.phoneDisplay}</a></p>
            <p><a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a></p>
            <p>WhatsApp: <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer" className="link-underline">Chat starten</a></p>
          </address>
          <Link to={`${ROUTES.kontakt}#formular`} className="btn btn--icon contact__cta">
            <IconMail />{contact.cta}
          </Link>
        </div>
      </div>
      {variant === 'home' && <Deco className="contact__deco" />}
    </section>
  );
}
