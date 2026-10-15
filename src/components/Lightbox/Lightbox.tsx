import { useCallback, useEffect, useRef } from 'react';
import { IconChevronLeft, IconChevronRight, IconClose } from '../Icons';
import '../LifestyleGallery/LifestyleGallery.css';

type Img = { src: string; alt: string; title?: string };

/** Vollbild-Bildansicht mit Tastatur (Esc, ←, →); Stil wie Lifestyle-Galerie */
export default function Lightbox({ images, index, onIndex, onClose }: { images: Img[]; index: number; onIndex: (i: number) => void; onClose: () => void }) {
  const closeRef = useRef<HTMLButtonElement>(null);
  const step = useCallback((d: number) => onIndex((index + d + images.length) % images.length), [index, images.length, onIndex]);
  useEffect(() => {
    document.body.classList.add('no-scroll');
    closeRef.current?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1); };
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('keydown', onKey); document.body.classList.remove('no-scroll'); };
  }, [onClose, step]);
  const img = images[index];
  return (
    <div className="lightbox" role="dialog" aria-modal="true" aria-label="Bildergalerie">
      <button type="button" className="lightbox__close" onClick={onClose} ref={closeRef} aria-label="Galerie schließen"><IconClose /></button>
      <button type="button" className="lightbox__nav lightbox__nav--prev" onClick={() => step(-1)} aria-label="Vorheriges Bild"><IconChevronLeft /></button>
      <figure className="lightbox__fig">
        <img src={img.src} alt={img.alt} />
        <figcaption><span className="head">{img.title ?? img.alt}</span><span className="lightbox__count">{index + 1} / {images.length}</span></figcaption>
      </figure>
      <button type="button" className="lightbox__nav lightbox__nav--next" onClick={() => step(1)} aria-label="Nächstes Bild"><IconChevronRight /></button>
    </div>
  );
}
