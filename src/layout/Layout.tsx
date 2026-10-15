import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../components/Header/Header';
import Footer from '../components/Footer/Footer';
import Toast from '../components/Toast/Toast';
import CookieSettings from '../components/Cookies/Cookies';
import RatingPanel from '../components/RatingPanel/RatingPanel';
import ContactWidget from '../components/ContactWidget/ContactWidget';
import Breadcrumb from '../components/Breadcrumb/Breadcrumb';
import { ScrollManager } from '../components/SmartLink/SmartLink';
import { usePageMetaValue } from './PageMeta';

export default function Layout() {
  const meta = usePageMetaValue();
  return (
    <>
      <ScrollManager />
      <Header />
      <main><Suspense fallback={<div className="page-loading" aria-busy="true" />}><Outlet /></Suspense></main>
      {meta.crumbs && <Breadcrumb items={meta.crumbs} />}
      <Footer variant={meta.footer ?? 'open'} />
      <Toast />
      <CookieSettings />
      <RatingPanel />
      <ContactWidget />
    </>
  );
}
