import SmartLink from '../SmartLink/SmartLink';
import './SplitCard.css';

type Props = { image: string; alt: string; title: string; text: string; cta: string; to?: string | null };

/** Bild/Text-Karte – Referenz: 1128×376, Bild 3:2 links (564px), cremefarbenes Textfeld rechts, Padding 72/48. */
export default function SplitCard({ image, alt, title, text, cta, to }: Props) {
  return (
    <div className="wrap">
      <article className="split">
        <div className="split__media"><img src={image} alt={alt} loading="lazy" /></div>
        <div className="split__body">
          <h2 className="split__title head">{title}</h2>
          <p className="split__text">{text}</p>
          <SmartLink label={cta} to={to} className="btn split__cta" />
        </div>
      </article>
    </div>
  );
}
