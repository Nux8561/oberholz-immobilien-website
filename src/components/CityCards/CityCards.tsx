import { cities } from '../../data/content';
import SectionIntro from '../SectionIntro/SectionIntro';
import { IconArrowRight } from '../Icons';
import SmartLink from '../SmartLink/SmartLink';
import './CityCards.css';

/** Städte – Referenz: Grid 3×360px (Gap 24), Card 360×316, Padding 16, Bild 328×220, H3 20/28, Sub 14/24. */
export default function CityCards() {
  return (
    <div className="wrap">
      <SectionIntro variant="inline" eyebrow={cities.eyebrow} title={cities.title} text={cities.text} id="staedte" />
      <div className="cities">
        {cities.items.map((c) => (
          <article key={c.name} className="city">
            <div className="city__media"><img src={c.image} alt={`Immobilien in ${c.name}`} loading="lazy" /></div>
            <div className="city__body">
              <h3 className="city__name head">{c.name}</h3>
              <p className="city__sub">{cities.subtitle}</p>
            </div>
            <SmartLink label={`Immobilien in ${c.name}`} to={c.to} className="city__link">
              <span className="sr-only">Immobilien in {c.name}</span>
              <IconArrowRight />
            </SmartLink>
          </article>
        ))}
      </div>
    </div>
  );
}
