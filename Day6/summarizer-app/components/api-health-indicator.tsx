'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

export default function ApiHealthIndicator() {
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      const isOnline = await apiClient.healthCheck();
      setApiOnline(isOnline);
    };
    
    checkHealth();
    
    // Recheck every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  if (apiOnline === null) {
    return (
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 bg-slate-400 rounded-full"></div>
        <span className="text-sm text-slate-600">Checking API...</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <div 
        className={`w-2 h-2 rounded-full ${
          apiOnline 
            ? 'bg-green-500 animate-pulse' 
            : 'bg-red-500'
        }`}
      />
      <span className={`text-sm ${
        apiOnline 
          ? 'text-green-600 font-medium' 
          : 'text-red-600 font-medium'
      }`}>
        {apiOnline ? 'API Online' : 'API Offline'}
      </span>
    </div>
  );
}