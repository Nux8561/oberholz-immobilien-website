import { homeFaq } from '../../data/siteFaq';
import { FaqBlock } from '../Rich/Rich';
import './OwnerHome.css';

/** Häufige Fragen auf der Startseite (gleiche Inhalte wie im FAQ-JSON-LD) */
export default function HomeFaq() {
  return <section className="wrap owner-home" aria-label="Häufige Fragen">
    <FaqBlock title="Ihre Fragen. Klare Antworten." items={homeFaq} />
  </section>;
}
