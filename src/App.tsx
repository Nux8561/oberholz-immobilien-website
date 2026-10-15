import { lazy, type ComponentType } from 'react';
import { BrowserRouter, Navigate, Route, Routes, useParams } from 'react-router-dom';
import { PageMetaProvider } from './layout/PageMeta';
import Layout from './layout/Layout';
import Home from './pages/Home';
import NotFound from './pages/NotFound';
// Unterseiten werden erst bei Bedarf geladen (kleineres Start-Bundle).
const Search = lazy(() => import('./pages/Search/Search'));
const Expose = lazy(() => import('./pages/Expose/Expose'));
const L = () => import('./pages/oberholz/Leistungen');
const S = () => import('./pages/oberholz/Service');
const R = () => import('./pages/oberholz/Ratgeber');
const I = () => import('./pages/oberholz/Immopedia');
const U = () => import('./pages/oberholz/Unternehmen');
const G = () => import('./pages/oberholz/Legal');
const pick = <M, K extends keyof M>(load: () => Promise<M>, key: K) =>
  lazy(() => load().then((m) => ({ default: m[key] as unknown as ComponentType })));

const Leistungen = pick(L, 'Leistungen'), Verkaufen = pick(L, 'Verkaufen'), Bewertung = pick(L, 'Bewertung'), Vermieten = pick(L, 'Vermieten');
const Rueckmietverkauf = pick(L, 'Rueckmietverkauf'), Finanzierung = pick(L, 'Finanzierung'), Vermarktung = pick(L, 'Vermarktung');
const Kapitalanlage = pick(L, 'Kapitalanlage'), WohnungKaufen = pick(L, 'WohnungKaufen'), Immotipp = pick(L, 'Immotipp');
const Service = pick(S, 'Service'), Budgetrechner = pick(S, 'Budgetrechner'), Finanzierungsrechner = pick(S, 'Finanzierungsrechner'), WertHebelRechner = pick(S, 'WertHebelRechner');
const Ratgeber = pick(R, 'Ratgeber'), RatgeberThema = pick(R, 'RatgeberThema'), Artikel = pick(R, 'Artikel'), Whitepaper = pick(R, 'Whitepaper'), Downloads = pick(R, 'Downloads');
const Immopedia = pick(I, 'Immopedia'), Begriff = pick(I, 'Begriff');
const UeberUns = pick(U, 'UeberUns'), Qualifikation = pick(U, 'Qualifikation'), Iso = pick(U, 'Iso'), Kontakt = pick(U, 'Kontakt');
const KontaktStadt = pick(U, 'KontaktStadt'), Regionen = pick(U, 'Regionen'), Region = pick(U, 'Region'), RegionVerkaufen = pick(U, 'RegionVerkaufen');
const MeinBereich = pick(G, 'MeinBereich'), Impressum = pick(G, 'Impressum'), Datenschutz = pick(G, 'Datenschutz'), CookieHinweise = pick(G, 'CookieHinweise');

/** Alte Pfade (erste Template-Version) leiten auf die neuen Seiten weiter. */
function RedirectCity() {
  const { city = '' } = useParams();
  return <Navigate to={['muenster', 'essen', 'bochum'].includes(city) ? `/regionen/${city}` : '/regionen'} replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <PageMetaProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="immobilien" element={<Navigate to="/immobilien/kaufen" replace />} />
            <Route path="immobilien/:mode" element={<Search />} />
            <Route path="expose/:id" element={<Expose />} />

            <Route path="leistungen" element={<Leistungen />} />
            <Route path="verkaufen" element={<Verkaufen />} />
            <Route path="bewertung" element={<Bewertung />} />
            <Route path="vermieten" element={<Vermieten />} />
            <Route path="rueckmietverkauf" element={<Rueckmietverkauf />} />
            <Route path="finanzierung" element={<Finanzierung />} />
            <Route path="vermarktung" element={<Vermarktung />} />
            <Route path="kapitalanlage" element={<Kapitalanlage />} />
            <Route path="wohnung-kaufen" element={<WohnungKaufen />} />
            <Route path="immotipp" element={<Immotipp />} />

            <Route path="service" element={<Service />} />
            <Route path="service/budgetrechner" element={<Budgetrechner />} />
            <Route path="service/finanzierungsrechner" element={<Finanzierungsrechner />} />
            <Route path="service/wert-hebel-rechner" element={<WertHebelRechner />} />

            <Route path="ratgeber" element={<Ratgeber />} />
            <Route path="ratgeber/thema/:cat" element={<RatgeberThema />} />
            <Route path="ratgeber/:slug" element={<Artikel />} />
            <Route path="whitepaper/:slug" element={<Whitepaper />} />
            <Route path="downloads" element={<Downloads />} />
            <Route path="immopedia" element={<Immopedia />} />
            <Route path="immopedia/:slug" element={<Begriff />} />

            <Route path="ueber-uns" element={<UeberUns />} />
            <Route path="ueber-uns/qualifikation" element={<Qualifikation />} />
            <Route path="ueber-uns/iso-9001" element={<Iso />} />
            <Route path="kontakt" element={<Kontakt />} />
            <Route path="kontakt/:city" element={<KontaktStadt />} />
            <Route path="regionen" element={<Regionen />} />
            <Route path="regionen/:city" element={<Region />} />
            <Route path="regionen/:city/verkaufen" element={<RegionVerkaufen />} />

            <Route path="mein-bereich" element={<MeinBereich />} />
            <Route path="impressum" element={<Impressum />} />
            <Route path="datenschutz" element={<Datenschutz />} />
            <Route path="cookie-hinweise" element={<CookieHinweise />} />

            {/* Weiterleitungen alter Pfade */}
            <Route path="commercial" element={<Navigate to="/kapitalanlage" replace />} />
            <Route path="magazin/*" element={<Navigate to="/ratgeber" replace />} />
            <Route path="standorte" element={<Navigate to="/regionen" replace />} />
            <Route path="stadt/:city" element={<RedirectCity />} />
            <Route path="makler-werden" element={<Navigate to="/ueber-uns" replace />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </PageMetaProvider>
    </BrowserRouter>
  );
}
