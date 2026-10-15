import { financeBanner as f } from '../data/content';
import { IconCaret } from '../components/Icons';
import SmartLink from '../components/SmartLink/SmartLink';
import './FinanceBanner.css';

/** Werbebanner – Referenz: volle Breite 1440×434 (Bildlink). Text links, Berater (freigestellt) rechts auf Creme. */
export default function FinanceBanner() {
  return (
    <div className="fbanner">
      <SmartLink label={f.link} to={f.to} className="fbanner__link" aria-label={f.link}>
        <img className="fbanner__img" src={f.image} alt={f.alt} loading="lazy" />
        <span className="fbanner__copy">
          <span className="fbanner__word">{f.wordmark.toUpperCase()}</span>
          <span className="fbanner__sub">{f.sub.toUpperCase()}</span>
          <span className="fbanner__claim">{f.claim}</span>
          <span className="fbanner__cta">{f.link}<IconCaret size={16} /></span>
        </span>
      </SmartLink>
    </div>
  );
}
