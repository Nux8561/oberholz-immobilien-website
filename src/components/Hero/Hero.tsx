import { useEffect, useState } from 'react';
import { hero } from '../../data/content';
import HeroCarousel from '../HeroCarousel/HeroCarousel';
import PropertySearch from '../PropertySearch/PropertySearch';
import { IconArrowRight } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import './Hero.css';

/** Gemessenes Scrollverhalten (≥960px): Section gleitet über ~220px Scroll um 16px nach oben,
 *  Teaser-Reihe blendet beim ersten Scrollen ein und rückt um 50px nach oben (überlappt den Slider). */
const LIFT = 16;
const LIFT_RANGE = 220;
const smooth = (t: number) => t * t * (3 - 2 * t);

export default function Hero() {
  const [lift, setLift] = useState(0);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    let raf = 0;
    const update = () => {
      raf = 0;
      const y = window.scrollY;
      setScrolled(y > 0);
      setLift(LIFT * smooth(Math.min(1, Math.max(0, y / LIFT_RANGE))));
    };
    const onScroll = () => { if (!raf) raf = requestAnimationFrame(update); };
    update();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => { window.removeEventListener('scroll', onScroll); cancelAnimationFrame(raf); };
  }, []);

  return (
    <section className={`hero${scrolled ? ' is-scrolled' : ''}`} style={{ '--hero-lift': `${-lift}px` } as React.CSSProperties} aria-label="Immobiliensuche">
      <div className="hero__head">
        <p className="hero__title head">{hero.title}</p>
        <PropertySearch />
      </div>
      <div className="hero__carousel"><HeroCarousel /></div>
      <div className="hero__teasers">
        {hero.teasers.map((t) => (
          <article key={t.title} className="hteaser">
            <img className="hteaser__img" src={t.image} alt="" width={60} height={60} />
            <p className="hteaser__title head">{t.title}</p>
            <SmartLink label={t.title} to={t.to} className="hteaser__link">
              <span className="sr-only">{t.label}</span>
              <IconArrowRight />
            </SmartLink>
          </article>
        ))}
      </div>
    </section>
  );
}
