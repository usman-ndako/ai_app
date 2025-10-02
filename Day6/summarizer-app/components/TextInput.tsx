import { useState } from 'react';

interface TextInputProps {
  value: string;
  onChange: (value: string) => void;
  onAnalyze: () => void;
  analyzing: boolean;
}

export default function TextInput({ value, onChange, onAnalyze, analyzing }: TextInputProps) {
  const [wordCount, setWordCount] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    onChange(text);
    setWordCount(text.trim() ? text.trim().split(/\s+/).length : 0);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <label htmlFor="text-input" className="block text-sm font-medium text-gray-700">
          Document Text
        </label>
        <div className="text-sm text-gray-500">
          {wordCount} words {value.length > 0 && `• ${value.length} characters`}
        </div>
      </div>
      
      <textarea
        id="text-input"
        value={value}
        onChange={handleChange}
        placeholder="Paste your document text here... (max 10,000 characters)"
        className="w-full h-64 p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        maxLength={10000}
      />
      
      <div className="flex gap-3">
        <button
          onClick={onAnalyze}
          disabled={!value.trim() || analyzing}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {analyzing ? 'Analyzing...' : 'Analyze Content'}
        </button>
        
        <div className="flex-1 text-xs text-gray-500 flex items-center">
          {value.length > 0 && (
            <span>
              Analyze to get AI recommendations for the best summary type
            </span>
          )}
        </div>
      </div>
    </div>
  );
}