// Darstellung der Oberholz Icons (Quelle: ./pack.ts). Linie bleibt ab 24 px bei 1,5 px (auch wenn CSS das Icon
// größer zieht), darunter wird sie proportional dünner.
import type { SVGProps } from 'react';
import { ICONS, type IconDef, type IconName } from './pack';

export type { IconName };

export type IconProps = Omit<SVGProps<SVGSVGElement>, 'name'> & {
  name: IconName;
  /** Breite in px (Höhe folgt dem Seitenverhältnis) */
  size?: number;
};

export function Icon({ name, size, strokeWidth, ...rest }: IconProps) {
  const def: IconDef = ICONS[name];
  const [w, h] = def.vb ?? [24, 24];
  const px = size ?? w;
  return (
    <svg
      width={px}
      height={Math.round((px * h) / w)}
      viewBox={`0 0 ${w} ${h}`}
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth ?? Math.min(1.5, Math.round(((1.5 * px) / 24) * 100) / 100)}
      strokeLinecap="butt"
      strokeLinejoin="miter"
      aria-hidden="true"
      focusable="false"
      {...rest}
    >
      {def.s && <path d={def.s} vectorEffect="non-scaling-stroke" />}
      {def.f && <path d={def.f} fill="currentColor" stroke="none" />}
      {def.a && <path d={def.a} className="oi-a" fill="currentColor" stroke="none" />}
    </svg>
  );
}
