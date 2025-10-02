import { SummaryResponse } from '@/types';
import { Copy, CheckCircle, Clock, Cpu } from 'lucide-react';
import { useState } from 'react';

interface SummaryOutputProps {
  summary: SummaryResponse | null;
  loading: boolean;
}

export default function SummaryOutput({ summary, loading }: SummaryOutputProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (summary?.summary) {
      await navigator.clipboard.writeText(summary.summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-8 text-center">
        <div className="animate-pulse space-y-4">
          <Clock className="mx-auto text-blue-500" size={48} />
          <div className="text-lg font-medium text-gray-700">Generating summary...</div>
          <div className="text-sm text-gray-500">This may take a few seconds</div>
        </div>
      </div>
    );
  }

  if (!summary) return null;

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Generated Summary</h3>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span className="capitalize px-2 py-1 bg-blue-100 text-blue-800 rounded">
              {summary.metadata.summary_type}
            </span>
            <span>{summary.metadata.summary_length} characters</span>
            <span>{summary.metadata.processing_time_seconds}s</span>
          </div>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          {copied ? <CheckCircle size={16} /> : <Copy size={16} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>

      <div className="prose max-w-none border-t pt-4">
        <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
          {summary.summary}
        </div>
      </div>

      <div className="border-t pt-4">
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <Cpu size={16} />
          <span>Model: {summary.metadata.model}</span>
          <span>•</span>
          <span>Technique: {summary.metadata.technique}</span>
        </div>
      </div>
    </div>
  );
}