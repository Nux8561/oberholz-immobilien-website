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
const O = () => import('./pages/oberholz/LocalOwner');
const pick = <M, K extends keyof M>(load: () => Promise<M>, key: K) =>
  lazy(() => load().then((m) => ({ default: m[key] as unknown as ComponentType })));

const Verkaufen = pick(L, 'Verkaufen'), Bewertung = pick(L, 'Bewertung'), Vermieten = pick(L, 'Vermieten');
const Rueckmietverkauf = pick(L, 'Rueckmietverkauf'), Finanzierung = pick(L, 'Finanzierung');
const Kapitalanlage = pick(L, 'Kapitalanlage'), Immotipp = pick(L, 'Immotipp');
const Budgetrechner = pick(S, 'Budgetrechner'), Finanzierungsrechner = pick(S, 'Finanzierungsrechner'), WertHebelRechner = pick(S, 'WertHebelRechner');
const Ratgeber = pick(R, 'Ratgeber'), RatgeberThema = pick(R, 'RatgeberThema'), Artikel = pick(R, 'Artikel'), Whitepaper = pick(R, 'Whitepaper');
const Immopedia = pick(I, 'Immopedia'), Begriff = pick(I, 'Begriff');
const UeberUns = pick(U, 'UeberUns'), Kontakt = pick(U, 'Kontakt');
const Regionen = pick(U, 'Regionen'), Region = pick(U, 'Region'), RegionVerkaufen = pick(U, 'RegionVerkaufen');
const MeinBereich = pick(G, 'MeinBereich'), Impressum = pick(G, 'Impressum'), Datenschutz = pick(G, 'Datenschutz'), CookieHinweise = pick(G, 'CookieHinweise');
const RegionBewertung = pick(O, 'RegionBewertung'), RegionWohnungVerkaufen = pick(O, 'RegionWohnungVerkaufen');

/** Alte Pfade leiten weiter. Münster hat keine eigene Stadtseite → Münsterland-Objekte. */
function RedirectCity() {
  const { city = '' } = useParams();
  if (city === 'muenster') return <Navigate to="/immobilien/kaufen?ort=M%C3%BCnsterland" replace />;
  return <Navigate to={['essen', 'bochum'].includes(city) ? `/regionen/${city}` : '/regionen'} replace />;
}

/** Frühere Kontakt-Stadtseiten → Standortseite der Stadt (Münster → Kontakt) */
function RedirectKontaktCity() {
  const { city = '' } = useParams();
  return <Navigate to={['essen', 'bochum'].includes(city) ? `/regionen/${city}` : '/kontakt'} replace />;
}

function RedirectMuensterAway({ to = '/regionen' }: { to?: string }) {
  return <Navigate to={to} replace />;
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

            <Route path="verkaufen" element={<Verkaufen />} />
            <Route path="bewertung" element={<Bewertung />} />
            <Route path="vermieten" element={<Vermieten />} />
            <Route path="rueckmietverkauf" element={<Rueckmietverkauf />} />
            <Route path="finanzierung" element={<Finanzierung />} />
            <Route path="kapitalanlage" element={<Kapitalanlage />} />
            <Route path="immotipp" element={<Immotipp />} />

            <Route path="service/budgetrechner" element={<Budgetrechner />} />
            <Route path="service/finanzierungsrechner" element={<Finanzierungsrechner />} />
            <Route path="service/wert-hebel-rechner" element={<WertHebelRechner />} />

            <Route path="ratgeber" element={<Ratgeber />} />
            <Route path="ratgeber/thema/:cat" element={<RatgeberThema />} />
            <Route path="ratgeber/:slug" element={<Artikel />} />
            <Route path="whitepaper/:slug" element={<Whitepaper />} />
            <Route path="immopedia" element={<Immopedia />} />
            <Route path="immopedia/:slug" element={<Begriff />} />

            <Route path="ueber-uns" element={<UeberUns />} />
            <Route path="kontakt" element={<Kontakt />} />
            <Route path="kontakt/:city" element={<RedirectKontaktCity />} />
            <Route path="regionen" element={<Regionen />} />
            <Route path="regionen/muenster" element={<RedirectMuensterAway to="/immobilien/kaufen?ort=M%C3%BCnsterland" />} />
            <Route path="regionen/muenster/verkaufen" element={<RedirectMuensterAway to="/verkaufen" />} />
            <Route path="regionen/:city" element={<Region />} />
            <Route path="regionen/:city/verkaufen" element={<RegionVerkaufen />} />
            <Route path="regionen/:city/immobilienbewertung" element={<RegionBewertung />} />
            <Route path="regionen/:city/wohnung-verkaufen" element={<RegionWohnungVerkaufen />} />

            <Route path="mein-bereich" element={<MeinBereich />} />
            <Route path="impressum" element={<Impressum />} />
            <Route path="datenschutz" element={<Datenschutz />} />
            <Route path="cookie-hinweise" element={<CookieHinweise />} />

            {/* Weiterleitungen alter Pfade (zusammengelegte Seiten, siehe SEITENSTRUKTUR.md) */}
            <Route path="leistungen" element={<Navigate to="/verkaufen" replace />} />
            <Route path="vermarktung" element={<Navigate to="/verkaufen" replace />} />
            <Route path="wohnung-kaufen" element={<Navigate to="/immobilien/kaufen?typ=Wohnung" replace />} />
            <Route path="service" element={<Navigate to="/ratgeber#rechner" replace />} />
            <Route path="downloads" element={<Navigate to="/ratgeber#downloads" replace />} />
            <Route path="ueber-uns/qualifikation" element={<Navigate to="/ueber-uns#qualifikation" replace />} />
            <Route path="ueber-uns/iso-9001" element={<Navigate to="/ueber-uns#qualitaet" replace />} />
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
