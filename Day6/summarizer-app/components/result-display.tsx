'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FiCopy, FiDownload, FiCheck } from 'react-icons/fi';
import { toast } from 'sonner';
import { SummaryResponse, SUMMARY_TYPES } from '@/lib/types';

interface ResultDisplayProps {
  result: SummaryResponse;
  originalText: string;
}

export default function ResultDisplay({ result, originalText }: ResultDisplayProps) {
  const [copied, setCopied] = useState(false);

  const summaryTypeConfig = SUMMARY_TYPES.find(
    (type) => type.value === result.metadata.summary_type
  );

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.summary);
      setCopied(true);
      toast.success('Summary copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast.error('Failed to copy to clipboard');
    }
  };

  const handleExportTxt = () => {
    const content = `
AI Document Summary
==================
Type: ${summaryTypeConfig?.label}
Generated: ${new Date().toLocaleString()}

Original Text (${result.metadata.original_length} characters):
${originalText}

Summary (${result.metadata.summary_length} characters):
${result.summary}

Metrics:
- Compression Ratio: ${result.metadata.compression_ratio}
- Processing Time: ${result.metadata.processing_time_seconds}s
- Model: ${result.metadata.model_version}
    `.trim();

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `summary-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Summary exported as TXT file!');
  };

  const handleExportJson = () => {
    const data = {
      summary: result.summary,
      metadata: result.metadata,
      original_text: originalText,
      generated_at: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `summary-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Summary exported as JSON file!');
  };

  return (
    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Summary Card */}
      <Card className="shadow-lg border-green-200 bg-green-50/50">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="text-3xl">{summaryTypeConfig?.icon}</div>
              <div>
                <CardTitle className="flex items-center gap-2">
                  Summary Generated
                  <Badge variant="secondary" className="bg-green-100 text-green-700">
                    {summaryTypeConfig?.label}
                  </Badge>
                </CardTitle>
                <CardDescription>{summaryTypeConfig?.description}</CardDescription>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="gap-2"
              >
                {copied ? (
                  <>
                    <FiCheck className="w-4 h-4 text-green-600" />
                    Copied!
                  </>
                ) : (
                  <>
                    <FiCopy className="w-4 h-4" />
                    Copy
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleExportTxt}
                className="gap-2"
              >
                <FiDownload className="w-4 h-4" />
                TXT
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleExportJson}
                className="gap-2"
              >
                <FiDownload className="w-4 h-4" />
                JSON
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="prose prose-slate max-w-none">
            <div className="bg-white p-6 rounded-lg border border-slate-200 text-slate-700 leading-relaxed">
              {result.summary}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Metrics Card */}
      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="text-lg">Performance Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricItem
              label="Original Length"
              value={`${result.metadata.original_length.toLocaleString()} chars`}
              icon="📄"
            />
            <MetricItem
              label="Summary Length"
              value={`${result.metadata.summary_length.toLocaleString()} chars`}
              icon="📝"
            />
            <MetricItem
              label="Compression"
              value={result.metadata.compression_ratio}
              icon="📊"
              highlight
            />
            <MetricItem
              label="Processing Time"
              value={`${result.metadata.processing_time_seconds}s`}
              icon="⚡"
            />
          </div>
          <div className="mt-4 pt-4 border-t border-slate-200">
            <p className="text-xs text-slate-500">
              Model: {result.metadata.model_version}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

interface MetricItemProps {
  label: string;
  value: string;
  icon: string;
  highlight?: boolean;
}

function MetricItem({ label, value, icon, highlight }: MetricItemProps) {
  return (
    <div className={`p-4 rounded-lg ${highlight ? 'bg-blue-50 border border-blue-200' : 'bg-slate-50'}`}>
      <div className="flex items-center gap-2 mb-1">
        <span className="text-xl">{icon}</span>
        <span className="text-xs text-slate-600 font-medium">{label}</span>
      </div>
      <div className={`text-lg font-bold ${highlight ? 'text-blue-600' : 'text-slate-900'}`}>
        {value}
      </div>
    </div>
  );
}