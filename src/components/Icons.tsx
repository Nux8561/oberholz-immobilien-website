// Oberholz Icons – Komfort-Exporte der Hausikonen (Quelle: src/icons/pack.ts, Formensprache „Fuge & Raute“).
import type { SVGProps } from 'react';
import { Icon, type IconName } from '../icons/Icon';

type P = Omit<SVGProps<SVGSVGElement>, 'name'> & { size?: number };
const make = (name: IconName) => (props: P) => <Icon name={name} {...props} />;

export const IconSearch = make('search');
export const IconChevronDown = make('chevron-down');
export const IconChevronUp = make('chevron-up');
export const IconChevronRight = make('chevron-right');
export const IconChevronLeft = make('chevron-left');
export const IconArrowRight = make('arrow-right');
export const IconUser = make('user');
export const IconGlobe = make('globe');
export const IconPin = make('pin');
export const IconBuildings = make('buildings');
export const IconSparkle = make('sparkle');
export const IconPause = make('pause');
export const IconPlay = make('play');
export const IconClose = make('close');
export const IconMenu = make('menu');
export const IconMail = make('mail');
export const IconExpand = make('expand');
export const IconPlus = make('plus');
export const IconMinus = make('minus');
export const IconCheck = make('check');
export const IconCaret = make('caret');
export const IconPhone = make('phone');
export const IconHeart = make('heart');
export const IconBell = make('bell');
export const IconSliders = make('sliders');
export const IconSort = make('sort');
export const IconShare = make('share');
export const IconImage = make('image');

/* ---------- Größere Motive (Rauten in Akzentfarbe über .oi-accent) ---------- */

export const BenefitIcon = ({ name, className = '', ...r }: { name: string } & P) => (
  <Icon name={name === 'pin' || name === 'globe' ? name : 'advisor'} size={48} className={`oi-accent ${className}`} {...r} />
);

const TOPICS = { house: 'ill-house', townhouse: 'ill-townhouse', apartment: 'ill-apartment' } as const;
export const TopicIllustration = ({ name, className = '', ...r }: { name: string } & P) => (
  <Icon name={TOPICS[name as keyof typeof TOPICS] ?? 'ill-apartment'} size={92} className={`oi-accent ${className}`} {...r} />
);

/* ---------- Social ---------- */
export const SocialIcon = ({ name }: { name: string }) => {
  const g: Record<string, JSX.Element> = {
    instagram: (<g fill="none" stroke="#fff" strokeWidth="1.5"><rect x="6" y="6" width="12" height="12" rx="3.5" /><circle cx="12" cy="12" r="2.8" /><circle cx="15.6" cy="8.4" r=".4" fill="#fff" /></g>),
    facebook: (<path fill="#fff" d="M13.2 19v-6h2l.3-2.4h-2.3V9.2c0-.7.2-1.2 1.2-1.2h1.2V5.9a16 16 0 0 0-1.8-.1c-1.8 0-3 1.1-3 3.1v1.7H8.8V13h2V19Z" />),
    linkedin: (<path fill="#fff" d="M6.5 9.5h2.4V18H6.5zM7.7 5.8a1.4 1.4 0 1 1 0 2.8 1.4 1.4 0 0 1 0-2.8ZM10.6 9.5h2.3v1.2c.4-.7 1.2-1.4 2.6-1.4 2.4 0 2.9 1.6 2.9 3.7V18H16v-4.4c0-1 0-2.4-1.5-2.4S13 12.4 13 13.5V18h-2.4Z" />),
    youtube: (<g><rect x="5" y="7.5" width="14" height="9.5" rx="2.4" fill="#fff" /><path d="m10.6 10 3.6 2.2-3.6 2.2Z" fill="#0d0d0d" /></g>),
    xing: (<path fill="#fff" d="M7.4 8.6h2.3l1.4 2.4-1.9 3.3H6.9l1.9-3.3-1.4-2.4Zm7.3-3.1H17l-3.4 6 2.2 4h-2.3l-2.2-4 3.4-6Z" />),
    google: (<path fill="#fff" d="M18.6 12.2c0-.5 0-1-.1-1.4H12v2.7h3.7a3.2 3.2 0 0 1-1.4 2.1v1.7h2.2c1.3-1.2 2.1-3 2.1-5.1ZM12 19c1.9 0 3.4-.6 4.5-1.7l-2.2-1.7c-.6.4-1.4.7-2.3.7-1.8 0-3.3-1.2-3.8-2.8H5.9v1.8A6.8 6.8 0 0 0 12 19Zm-3.8-5.5a4 4 0 0 1 0-2.6V9.1H5.9a6.8 6.8 0 0 0 0 6.2l2.3-1.8ZM12 7.7c1 0 1.9.4 2.6 1l2-1.9A6.8 6.8 0 0 0 5.9 9.1l2.3 1.8c.5-1.6 2-3.2 3.8-3.2Z" />),
    whatsapp: (<path fill="#fff" d="M12 4.6a7.3 7.3 0 0 0-6.3 11l-.9 3.4 3.5-.9A7.3 7.3 0 1 0 12 4.6Zm0 13.3c-1.1 0-2.2-.3-3.1-.9l-.2-.1-2 .5.5-2-.1-.2a6 6 0 1 1 4.9 2.7Zm3.3-4.5c-.2-.1-1.1-.5-1.2-.6-.2-.1-.3-.1-.4.1l-.6.7c-.1.1-.2.1-.4 0a4.9 4.9 0 0 1-2.4-2.1c-.2-.3.2-.3.5-1 .1-.1 0-.2 0-.3l-.5-1.3c-.1-.3-.3-.3-.4-.3h-.4a.7.7 0 0 0-.5.3c-.2.2-.7.7-.7 1.6s.7 1.9.8 2c.1.1 1.4 2.2 3.4 3 1.3.5 1.8.6 2.4.5.4-.1 1.1-.5 1.3-.9.2-.4.2-.8.1-.9l-.4-.2Z" />),
    tiktok: (<path fill="#fff" d="M13.8 5.5h2c.2 1.5 1.1 2.5 2.7 2.6v2c-1 0-1.9-.3-2.7-.8v4.4a3.9 3.9 0 1 1-3.9-3.9h.4v2.1h-.4a1.8 1.8 0 1 0 1.9 1.8Z" />),
  };
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0d0d0d" />{g[name]}</svg>
  );
};
