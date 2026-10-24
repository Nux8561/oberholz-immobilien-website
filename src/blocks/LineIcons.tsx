// Inhalts-Icons (Vorteile, Schritte, Kennzahlen, Leistungen) aus dem Oberholz-Icon-Set; Rauten in Akzentfarbe.
import { Icon } from '../icons/Icon';
import type { IconName } from '../icons/pack';

export type LineIconName = Extract<IconName,
  | 'phone' | 'pin' | 'globe' | 'advisor' | 'house' | 'apartment' | 'multi' | 'sale' | 'star' | 'compass' | 'chart'
  | 'document' | 'camera' | 'megaphone' | 'key' | 'people' | 'academy' | 'tools' | 'money' | 'shield' | 'calendar'
  | 'award' | 'sun' | 'signature' | 'hand' | 'bulb' | 'eye'>;

export function LineIcon({ name, size = 24 }: { name: LineIconName; size?: number }) {
  return <Icon name={name} size={size} className="line-icon oi-accent" />;
}
