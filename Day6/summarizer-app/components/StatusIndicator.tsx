import { ApiStatus } from '@/types';
import { Wifi, WifiOff, Clock } from 'lucide-react';

interface StatusIndicatorProps {
  status: ApiStatus;
}

export default function StatusIndicator({ status }: StatusIndicatorProps) {
  const getStatusConfig = () => {
    switch (status) {
      case 'online':
        return { icon: Wifi, color: 'text-green-500', bg: 'bg-green-100', text: 'API Online' };
      case 'offline':
        return { icon: WifiOff, color: 'text-red-500', bg: 'bg-red-100', text: 'API Offline' };
      default:
        return { icon: Clock, color: 'text-yellow-500', bg: 'bg-yellow-100', text: 'Checking...' };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${config.bg} ${config.color}`}>
      <Icon size={16} />
      <span className="text-sm font-medium">{config.text}</span>
    </div>
  );
}