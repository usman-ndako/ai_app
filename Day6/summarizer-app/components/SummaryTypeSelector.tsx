import { SummaryTypes } from '@/types';
import { FileText, Briefcase, Scale, Cpu, TrendingUp } from 'lucide-react';

interface SummaryTypeSelectorProps {
  summaryTypes: SummaryTypes;
  selectedType: string;
  onTypeSelect: (type: string) => void;
}

const typeIcons = {
  standard: FileText,
  executive: Briefcase,
  legal: Scale,
  technical: Cpu,
  financial: TrendingUp,
};

export default function SummaryTypeSelector({ 
  summaryTypes, 
  selectedType, 
  onTypeSelect 
}: SummaryTypeSelectorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
      {Object.entries(summaryTypes).map(([type, config]) => {
        const Icon = typeIcons[type as keyof typeof typeIcons];
        return (
          <div
            key={type}
            className={`border-2 rounded-xl p-4 cursor-pointer transition-all duration-300 hover:shadow-lg ${
              selectedType === type
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => onTypeSelect(type)}
          >
            <div className="flex items-center gap-3 mb-2">
              <Icon size={20} className="text-blue-500" />
              <h3 className="font-semibold text-gray-900 capitalize">{type}</h3>
            </div>
            <p className="text-sm text-gray-600">{config.description}</p>
          </div>
        );
      })}
    </div>
  );
}