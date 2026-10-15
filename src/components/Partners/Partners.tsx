import { partners } from '../../data/content';
import SectionIntro from '../SectionIntro/SectionIntro';
import './Partners.css';

type Kind = keyof typeof partners;
const TEXT: Record<Kind, { eyebrow: string; title: string; text: string }> = {
  kooperation: { eyebrow: 'Kooperationen', title: 'Starke Partner an unserer Seite', text: 'Für Finanzierung, Vorsorge und Absicherung arbeiten wir mit etablierten Partnern zusammen – so erhalten Sie alles aus einer Hand.' },
  finanzierung: { eyebrow: 'Finanzierungspartner', title: 'Unsere Finanzierungspartner', text: 'Über unser Banken-Netzwerk vergleichen wir Angebote und finden die Finanzierung, die zu Ihnen passt.' },
  portale: { eyebrow: 'Reichweite', title: 'Ihre Immobilie auf führenden Portalen', text: 'Neben unserem Käufernetzwerk präsentieren wir Ihre Immobilie auf reichweitenstarken Immobilienportalen.' },
};

/** Logo-Leiste für Kooperationen, Finanzierungspartner oder Portale (Logos der bisherigen Website). */
export default function Partners({ kinds, id }: { kinds: Kind[]; id?: string }) {
  return (
    <section className="wrap partners" id={id}>
      {kinds.map((k) => (
        <div key={k} className="partners__group">
          <SectionIntro variant="inline" line={false} eyebrow={TEXT[k].eyebrow} title={TEXT[k].title} text={TEXT[k].text} />
          <ul className="partners__logos">
            {partners[k].map((p) => {
              const img = <img src={p.logo} alt={p.name} loading="lazy" />;
              return <li key={p.name}>{'url' in p && p.url ? <a href={p.url} target="_blank" rel="noopener noreferrer" title={p.name}>{img}</a> : <span title={p.name}>{img}</span>}</li>;
            })}
          </ul>
        </div>
      ))}
    </section>
  );
}
