import { brand, contact, hubOffices, team, whatsappUrl } from '../../data/content';
import SectionIntro from '../SectionIntro/SectionIntro';
import { IconMail } from '../Icons';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../data/routes';
import Deco from '../Deco/Deco';
import './Contact.css';

function personFor(name?: string) {
  return team.find((m) => m.name === name);
}

export default function Contact({ variant = 'home' }: { variant?: 'home' | 'page' }) {
  const hubs = hubOffices();
  return (
    <section className={`contact contact--${variant}`} id="kontakt" aria-labelledby="kontakt-title">
      <div className="contact__inner">
        <div className="wrap contact__wrap">
          <SectionIntro variant="inline" line={false} center eyebrow={contact.eyebrow} id="kontakt-title"
            title={<>{contact.title.split(' – ')[0]} –<br />{contact.title.split(' – ')[1]}</>} />
          <div className="contact__hubs">
            {hubs.map((o) => {
              const person = personFor(o.contactName);
              return (
                <address key={o.slug} className="contact__address">
                  {person && (
                    <img className="contact__face" src={person.face} alt={person.name} width={72} height={72} />
                  )}
                  <p className="contact__office head">{o.city}</p>
                  {person && <p className="contact__person">{person.name}</p>}
                  <p>{o.street}</p>
                  <p>{o.zipCity}</p>
                  <p>Tel: <a href={o.phoneHref} className="link-underline">{o.phoneDisplay}</a></p>
                </address>
              );
            })}
          </div>
          <span className="contact__line" aria-hidden="true" />
          <p className="contact__shared">
            <a href={`mailto:${brand.email}`} className="link-underline">{brand.email}</a>
            <span aria-hidden="true"> · </span>
            WhatsApp: <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer" className="link-underline">{brand.whatsappDisplay}</a>
          </p>
          <Link to={`${ROUTES.kontakt}#formular`} className="btn btn--icon contact__cta">
            <IconMail />{contact.cta}
          </Link>
        </div>
      </div>
      {variant === 'home' && <Deco className="contact__deco" />}
    </section>
  );
}
