import { selling } from '../data/content';
import SectionIntro from '../components/SectionIntro/SectionIntro';
import SplitCard from '../components/SplitCard/SplitCard';
import { BenefitIcon } from '../components/Icons';
import './Selling.css';

export default function Selling() {
  return (
    <>
      <SectionIntro level="h1" eyebrow={selling.eyebrow} title={selling.title} text={selling.text} id="verkaufen" />
      <div className="wrap">
        <ul className="benefits">
          {selling.benefits.map((b) => (
            <li key={b.title} className="benefits__item">
              <BenefitIcon name={b.icon} className="benefits__icon" />
              <h2 className="benefits__title head">{b.title}</h2>
              <p className="benefits__text">{b.text}</p>
            </li>
          ))}
        </ul>
      </div>
      <SplitCard {...selling.card} />
    </>
  );
}
