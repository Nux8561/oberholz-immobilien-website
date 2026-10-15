// Eigene Linien-Icons (24×24, currentColor) – Strichstärke/Größen nach Referenz gemessen.
import type { SVGProps } from 'react';

type P = SVGProps<SVGSVGElement> & { size?: number };

const base = (size = 24, rest: SVGProps<SVGSVGElement>) => ({
  width: size,
  height: size,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.25,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
  'aria-hidden': true,
  focusable: false,
  ...rest,
});

export const IconSearch = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><circle cx="10.5" cy="10.5" r="6.5" /><path d="M15.3 15.3 20 20" /></svg>
);
export const IconChevronDown = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="m5 9 7 7 7-7" /></svg>);
export const IconChevronUp = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="m5 15 7-7 7 7" /></svg>);
export const IconChevronRight = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="m9 5 7 7-7 7" /></svg>);
export const IconChevronLeft = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="m15 5-7 7 7 7" /></svg>);
export const IconArrowRight = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><path d="M3.5 12h17M14.5 6l6 6-6 6" /></svg>
);
export const IconUser = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><circle cx="12" cy="12" r="9" /><circle cx="12" cy="10" r="3.2" /><path d="M6.3 18.6c1.3-2.3 3.3-3.4 5.7-3.4s4.4 1.1 5.7 3.4" /></svg>
);
export const IconGlobe = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3Z" /></svg>
);
export const IconPin = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><path d="M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21Z" /><circle cx="12" cy="9.8" r="2.4" /></svg>
);
export const IconBuildings = ({ size, ...r }: P) => (
  <svg {...base(size, r)}>
    <path d="M3.5 20.5V5.5l7-2v17M10.5 20.5V9.5l7 2.2v8.8M17.5 20.5h3V13l-3-1.3M2.5 20.5h19" />
    <path d="M5.8 7.8h2M5.8 10.8h2M5.8 13.8h2M5.8 16.8h2M12.8 13h2.4M12.8 16h2.4" />
  </svg>
);
export const IconSparkle = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><path d="M12 3.5c.6 4.4 2.1 5.9 6.5 6.5-4.4.6-5.9 2.1-6.5 6.5-.6-4.4-2.1-5.9-6.5-6.5 4.4-.6 5.9-2.1 6.5-6.5Z" /></svg>
);
export const IconPause = ({ size, ...r }: P) => (
  <svg {...base(size, r)} stroke="none" fill="currentColor"><rect x="7" y="5" width="3.2" height="14" rx=".4" /><rect x="13.8" y="5" width="3.2" height="14" rx=".4" /></svg>
);
export const IconPlay = ({ size, ...r }: P) => (
  <svg {...base(size, r)} stroke="none" fill="currentColor"><path d="M8 5.2v13.6a.5.5 0 0 0 .76.43l11.2-6.8a.5.5 0 0 0 0-.86L8.76 4.77A.5.5 0 0 0 8 5.2Z" /></svg>
);
export const IconClose = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="m5 5 14 14M19 5 5 19" /></svg>);
export const IconMenu = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="M3 6.5h14M3 12h18M3 17.5h10" /></svg>);
export const IconMail = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><rect x="3" y="5.5" width="18" height="13" rx=".5" /><path d="m3.5 6.5 8.5 6.5 8.5-6.5" /></svg>
);
export const IconExpand = ({ size, ...r }: P) => (
  <svg {...base(size, r)}><path d="M14 4h6v6M20 4l-7 7M10 20H4v-6M4 20l7-7" /></svg>
);
export const IconPlus = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="M12 4v16M4 12h16" /></svg>);
export const IconMinus = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="M4 12h16" /></svg>);
export const IconCheck = ({ size, ...r }: P) => (<svg {...base(size, r)}><path d="m4.5 12.5 4.5 4.5L19.5 6.5" /></svg>);
export const IconCaret = ({ size, ...r }: P) => (
  <svg {...base(size, r)} stroke="none" fill="currentColor"><path d="M9 7.5v9l6-4.5-6-4.5Z" /></svg>
);

/* ---------- Illustrative Icons (eigene Zeichnungen) ---------- */

const illu = (w: number, h: number, rest: SVGProps<SVGSVGElement>) => ({
  width: w, height: h, viewBox: `0 0 ${w} ${h}`, fill: 'none', stroke: 'currentColor', strokeWidth: 1.2,
  strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, 'aria-hidden': true, ...rest,
});

export const BenefitIcon = ({ name, ...r }: { name: string } & SVGProps<SVGSVGElement>) => {
  if (name === 'pin')
    return (<svg {...illu(48, 48, r)}><path d="M24 45S10 31.6 10 19.5a14 14 0 0 1 28 0C38 31.6 24 45 24 45Z" /><circle cx="24" cy="19.5" r="6.5" /></svg>);
  if (name === 'globe')
    return (
      <svg {...illu(48, 48, r)}>
        <circle cx="24" cy="24" r="13" /><path d="M11 24h26M24 11c3.6 3.6 5.4 8 5.4 13S27.6 33.4 24 37c-3.6-3.6-5.4-8-5.4-13S20.4 14.6 24 11ZM13.5 17h21M13.5 31h21" />
        <path d="M6.5 20A18 18 0 0 1 38 9.5M38 5v4.5h-4.5M41.5 28A18 18 0 0 1 10 38.5M10 43v-4.5h4.5" />
      </svg>
    );
  return (
    <svg {...illu(48, 48, r)}>
      <circle cx="24" cy="9" r="5.5" /><path d="M14 46V27c0-5 3.5-9 10-9s10 4 10 9v19" />
      <path d="M21 18.5 24 31l3-12.5M22.5 21.5h3" /><path d="M24 31v15M18.5 30v16M29.5 30v16" />
    </svg>
  );
};

export const TopicIllustration = ({ name, ...r }: { name: string } & SVGProps<SVGSVGElement>) => {
  if (name === 'house')
    return (
      <svg {...illu(92, 92, r)} strokeWidth={1}>
        <path d="M24 72V44L50 26l26 18v28" /><path d="M20 47 50 25l30 22" /><circle cx="50" cy="42" r="4" />
        <path d="M45 72V58h10v14M6 72h82M6 72V52h18M10 57h10v6H10z" /><path d="M14 52v-6h4v6" />
      </svg>
    );
  if (name === 'townhouse')
    return (
      <svg {...illu(92, 92, r)} strokeWidth={1}>
        <path d="M12 76V36h22v40M34 76V28h24v48M58 76V36h22v40M8 76h76" /><path d="M42 28l4-6 4 6" />
        {[16, 25, 62, 71].map((x) => [44, 54].map((y) => <rect key={`${x}-${y}`} x={x} y={y} width="5" height="6" />))}
        {[40, 48].map((x) => [36, 44, 52].map((y) => <rect key={`${x}-${y}`} x={x} y={y} width="5" height="5" />))}
        <path d="M18 76v-9h4v9M41 76v-11h10v11M66 76v-9h4v9" />
      </svg>
    );
  return (
    <svg {...illu(92, 92, r)} strokeWidth={1}>
      <path d="M26 76V22h40v54M22 76h48M32 22v-6h28v6" /><circle cx="46" cy="19" r="2" />
      {[32, 49].map((x) => [28, 38, 48].map((y) => <rect key={`${x}-${y}`} x={x} y={y} width="11" height="6" />))}
      <path d="M33 76V60h8v16M49 60h11v8H49z" />
    </svg>
  );
};

/** Eigene Fassadenzeichnung für den Footer (240×100). */
export const FooterIllustration = (r: SVGProps<SVGSVGElement>) => (
  <svg {...illu(240, 100, r)} strokeWidth={0.9} viewBox="0 0 240 100">
    <path d="M8 98h224M14 98V52h212v46M4 52h232L198 18H42Z" />
    {Array.from({ length: 34 }, (_, i) => <path key={i} d={`M${48 + i * 4.3} 20.5 ${30 + i * 5.4} 51`} strokeWidth={0.5} />)}
    <path d="M100 18c0-8 9-12 20-12s20 4 20 12" /><path d="M108 18v-4h24v4" />
    {[34, 76, 146, 188].map((x) => (
      <g key={x}><rect x={x} y={62} width={18} height={26} /><path d={`M${x + 9} 62v26M${x} 75h18`} /><path d={`M${x - 3} 60h24M${x - 3} 90h24`} /></g>
    ))}
    <path d="M110 98V70a10 10 0 0 1 20 0v28M110 80h20M120 70v28" />
    {[60, 102, 138, 180].map((x) => <path key={x} d={`M${x} 56v42M${x + 3} 56v42`} />)}
  </svg>
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
