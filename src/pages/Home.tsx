import Hero from '../components/Hero/Hero';
import Selling from '../sections/Selling';
import FinanceBanner from '../sections/FinanceBanner';
import CityCards from '../components/CityCards/CityCards';
import { Careers, Lifestyle, Magazine } from '../sections/Lifestyle';
import RelatedTopics from '../components/RelatedTopics/RelatedTopics';
import Contact from '../components/Contact/Contact';
import { faqLd, usePageMeta } from '../layout/PageMeta';
import { homeFaq } from '../data/oberholz';

// Reihenfolge exakt wie Referenz-<main> (15 Abschnitte)
export default function Home() {
  usePageMeta({ jsonLd: [faqLd(homeFaq)] });
  return (
    <>
      <Hero />
      <Selling />
      <FinanceBanner />
      <CityCards />
      <Careers />
      <Lifestyle />
      <Magazine />
      <RelatedTopics />
      <Contact />
    </>
  );
}
