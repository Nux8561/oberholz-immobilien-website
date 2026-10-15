// Eigene Linien-Icons (Raster 24, skaliert) für Vorteile, Schritte, Kennzahlen und Hero-Optionen.
const PATHS = {
  phone: 'M7.5 3.5h-3a1 1 0 0 0-1 1C3.5 13 11 20.5 19.5 20.5a1 1 0 0 0 1-1v-3l-4-1.5-2 2c-2.5-1-5-3.5-6-6l2-2Z',
  pin: 'M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21ZM12 7.4a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8Z',
  globe: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18ZM3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3Z',
  advisor: 'M12 2.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6ZM6.5 21.5V14c0-2.6 1.9-4.5 5.5-4.5s5.5 1.9 5.5 4.5v7.5M11 9.6l1 5 1-5',
  house: 'M3.5 11 12 4l8.5 7M6 9.5V20h12V9.5M10 20v-5h4v5',
  apartment: 'M6 21V3h12v18M3 21h18M9 6h2M13 6h2M9 9.5h2M13 9.5h2M9 13h2M13 13h2M10.5 21v-4h3v4',
  multi: 'M2.5 21h19M4 21V9h6v12M10 21V5h10v16M6 12h2M6 15h2M13 8h2M17 8h1M13 11h2M17 11h1M13 14h2M17 14h1M14 21v-3h2v3',
  handshake: 'M2.5 12 6 8.5l3 1.5 3-2 6 5-2 2-3-2.5M2.5 12l4.5 4.5 2-1.5 2 2 2-1.5M18 13.5l3.5-3.5-3-3-3 1.5',
  star: 'm12 3.2 2.6 5.5 6 .8-4.4 4.1 1.1 5.9L12 16.6l-5.3 2.9 1.1-5.9-4.4-4.1 6-.8Z',
  compass: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18ZM15.5 8.5l-2 5-5 2 2-5Z',
  chart: 'M3.5 20.5h17M6 20.5V13M10 20.5V9M14 20.5v-6M18 20.5V6',
  document: 'M6 2.5h8l4 4v15H6ZM14 2.5v4h4M9 11h6M9 14h6M9 17h4',
  camera: 'M3 7.5h4l1.5-2h7L17 7.5h4V19H3ZM12 9.5a3.8 3.8 0 1 0 0 7.6 3.8 3.8 0 0 0 0-7.6Z',
  megaphone: 'M3.5 10v4h3l7 4V6l-7 4ZM6.5 14l1.5 5h2.5l-1.5-5M17 9.5a3 3 0 0 1 0 5',
  key: 'M14.5 3.5a5 5 0 1 0 0 10 5 5 0 0 0 0-10ZM10.6 11.6 3.5 18.7v2h2.5l1-1h2v-2h2l1.5-1.5M16 7.5h0',
  people: 'M8.5 4.5a2.8 2.8 0 1 0 0 5.6 2.8 2.8 0 0 0 0-5.6ZM3.5 19.5c0-3.3 2.2-5.5 5-5.5s5 2.2 5 5.5M16 6a2.4 2.4 0 1 0 0 4.8M15.5 14c2.8 0 5 2 5 5.5',
  academy: 'M2.5 9 12 4.5 21.5 9 12 13.5ZM6.5 11v5c1.5 1.5 3.5 2.3 5.5 2.3s4-.8 5.5-2.3v-5M21.5 9v5',
  tools: 'M4 5.5h16v11H4ZM9 20h6M12 16.5V20M7 9h4M7 12h7',
  money: 'M3 7h18v10H3ZM12 9.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM6 10v4M18 10v4',
  shield: 'M12 3 4.5 6v5.5c0 4.5 3.2 8 7.5 9.5 4.3-1.5 7.5-5 7.5-9.5V6Z M8.5 12l2.5 2.5 4.5-5',
  calendar: 'M4 5.5h16v15H4ZM4 10h16M8 3v5M16 3v5',
  award: 'M12 3a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11ZM8.5 13l-1.5 8 5-2.5 5 2.5-1.5-8',
  sun: 'M12 7.5a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9ZM12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4',
  signature: 'M3 17c3-6 5-9 6.5-9 2 0-1 9 1.5 9 1.6 0 2.5-3 3.5-3 1 0 1 2 2.5 2s1.8-1 3-1M3 21h18',
  hand: 'M3 20h4l5 1.5 8-4-1.5-1.5L12 17.5M7 20v-6l5-2 4 1.5M12 10.5V4h6v7',
  bulb: 'M9 17.5h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9V17.5h7v-3.6A6 6 0 0 0 12 3Z',
  eye: 'M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12ZM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z',
} as const;

export type LineIconName = keyof typeof PATHS;

export function LineIcon({ name, size = 24 }: { name: LineIconName; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={size > 30 ? 0.7 : 1.1}
      strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="line-icon">
      <path d={PATHS[name]} />
    </svg>
  );
}
