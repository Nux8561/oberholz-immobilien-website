import Hero from '../components/Hero/Hero';
import Selling from '../sections/Selling';
import CityCards from '../components/CityCards/CityCards';
import { Careers, Lifestyle, Magazine } from '../sections/Lifestyle';
import HomeFaq from '../components/OwnerHome/OwnerHome';
import Contact from '../components/Contact/Contact';
import { faqLd, usePageMeta } from '../layout/PageMeta';
import { homeFaq } from '../data/siteFaq';

/** Startseite – bewusst kurz: Suche, Verkauf, Vermittlungen, Standorte, Team, Ratgeber, Fragen, Kontakt. */
export default function Home() {
  usePageMeta({ jsonLd: [faqLd(homeFaq)] });
  return (
    <>
      <Hero />
      <Selling />
      <Lifestyle />
      <CityCards />
      <Careers />
      <Magazine />
      <HomeFaq />
      <Contact />
    </>
  );
}
