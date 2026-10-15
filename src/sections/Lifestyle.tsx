import { careers, lifestyle, magazine } from '../data/content';
import SectionIntro from '../components/SectionIntro/SectionIntro';
import SplitCard from '../components/SplitCard/SplitCard';
import LifestyleGallery from '../components/LifestyleGallery/LifestyleGallery';

export function Careers() {
  return (
    <>
      <SectionIntro eyebrow={careers.eyebrow} title={careers.title} text={careers.text} id="karriere" />
      <SplitCard {...careers.card} />
    </>
  );
}

export function Lifestyle() {
  return (
    <>
      <SectionIntro title={lifestyle.title} text={lifestyle.text} id="lifestyle" />
      <LifestyleGallery />
    </>
  );
}

export function Magazine() {
  return (
    <>
      <SectionIntro eyebrow={magazine.eyebrow} title={magazine.title} text={magazine.text} id="magazin" />
      <SplitCard {...magazine.card} />
    </>
  );
}
