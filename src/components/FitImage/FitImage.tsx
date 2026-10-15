import { useState } from 'react';
import './FitImage.css';

/** Bild, das Hochformate nicht beschneidet: Querformate füllen den Rahmen, Hochformate werden vollständig
 *  gezeigt – auf einer weich verschwommenen Vergrößerung desselben Fotos statt auf grauem Rand. */
export default function FitImage({ src, alt, eager = false, className = '' }: { src: string; alt: string; eager?: boolean; className?: string }) {
  const [portrait, setPortrait] = useState(false);
  return (
    <span className={`fitimg${portrait ? ' is-portrait' : ''} ${className}`}>
      {portrait && <img className="fitimg__bg" src={src} alt="" aria-hidden="true" />}
      <img className="fitimg__fg" src={src} alt={alt} loading={eager ? 'eager' : 'lazy'} draggable={false}
        onLoad={(e) => { const i = e.currentTarget; if (i.naturalHeight > i.naturalWidth * 0.9) setPortrait(true); }} />
    </span>
  );
}
