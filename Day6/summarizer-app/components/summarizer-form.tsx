'use client';

import { useState } from 'react';
import { toast } from 'sonner';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FiSend, FiUpload } from 'react-icons/fi';
import { apiClient } from '@/lib/api';
import { SummaryType, SUMMARY_TYPES, SummaryResponse } from '@/lib/types';
import ResultDisplay from './result-display';
import FileUpload from './file-upload';
import LoadingSkeleton from './loading-skeleton';

const MAX_CHARS = 10000;

export default function SummarizerForm() {
  const [text, setText] = useState('');
  const [summaryType, setSummaryType] = useState<SummaryType>('executive');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SummaryResponse | null>(null);
  const [showFileUpload, setShowFileUpload] = useState(false);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value;
    if (newText.length <= MAX_CHARS) {
      setText(newText);
    }
  };

  const handleFileText = (fileText: string) => {
    if (fileText.length <= MAX_CHARS) {
      setText(fileText);
      setShowFileUpload(false);
      toast.success('File loaded successfully!');
    } else {
      toast.error(`File too large. Maximum ${MAX_CHARS.toLocaleString()} characters allowed.`);
    }
  };

  const handleSummarize = async () => {
  if (!text.trim()) {
    toast.error('Please enter some text to summarize');
    return;
  }

  if (text.length < 50) {
    toast.error('Text is too short. Please enter at least 50 characters.');
    return;
  }

  setIsLoading(true);
  setResult(null);

  try {
    const response = await apiClient.summarize({
      text: text,
      summary_type: summaryType,
    });

    setResult(response);
    toast.success('Summary generated successfully!');
  } catch (error) {
    if (error instanceof Error) {
      if (error.message.includes('fetch')) {
        toast.error('Cannot connect to API. Please ensure the backend is running on http://127.0.0.1:8000');
      } else {
        toast.error(error.message);
      }
    } else {
      toast.error('Failed to generate summary. Please try again.');
    }
  } finally {
    setIsLoading(false);
  }
};

  const handleClear = () => {
    setText('');
    setResult(null);
    toast.info('Cleared');
  };

  const charPercentage = (text.length / MAX_CHARS) * 100;
  const isNearLimit = charPercentage > 80;

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Input Card */}
      <Card className="shadow-lg border-slate-200">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Document Input</CardTitle>
              <CardDescription>
                Paste your document or upload a text file
              </CardDescription>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowFileUpload(!showFileUpload)}
              className="gap-2"
            >
              <FiUpload className="w-4 h-4" />
              Upload File
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* File Upload Section */}
          {showFileUpload && (
            <FileUpload onFileRead={handleFileText} />
          )}

          {/* Text Input */}
          <div className="space-y-2">
            <Label htmlFor="document-text">Document Text</Label>
            <Textarea
                id="document-text"
                placeholder="Paste your document here... (reports, contracts, articles, etc.)
                Press Enter to submit"
                value={text}
                onChange={handleTextChange}
                onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey && text.trim()) {
                    e.preventDefault();
                    handleSummarize();
                    }
                }}
                className="min-h-[300px] resize-none font-mono text-sm"
                disabled={isLoading}
                />
            <div className="flex items-center justify-between text-sm">
              <span className={`${isNearLimit ? 'text-orange-600 font-medium' : 'text-slate-500'}`}>
                {text.length.toLocaleString()} / {MAX_CHARS.toLocaleString()} characters
              </span>
              {text.length > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleClear}
                  disabled={isLoading}
                >
                  Clear
                </Button>
              )}
            </div>
            {/* Character progress bar */}
            <div className="w-full bg-slate-200 rounded-full h-1.5">
              <div
                className={`h-1.5 rounded-full transition-all ${
                  isNearLimit ? 'bg-orange-500' : 'bg-blue-500'
                }`}
                style={{ width: `${Math.min(charPercentage, 100)}%` }}
              />
            </div>
          </div>

          {/* Summary Type Selector */}
          <div className="space-y-2">
            <Label htmlFor="summary-type">Summary Type</Label>
            <Select
              value={summaryType}
              onValueChange={(value) => setSummaryType(value as SummaryType)}
              disabled={isLoading}
            >
              <SelectTrigger id="summary-type" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-white">
                {SUMMARY_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value} className="bg-white hover:bg-slate-100">
                    <div className="flex items-center gap-2">
                        <span>{type.icon}</span>
                        <div className="text-left">
                        <div className="font-medium">{type.label}</div>
                        <div className="text-xs text-slate-500">{type.description}</div>
                        </div>
                    </div>
                    </SelectItem>
                ))}
                </SelectContent>
            </Select>
          </div>

          {/* Summarize Button */}
          <Button
            onClick={handleSummarize}
            disabled={isLoading || !text.trim()}
            className="w-full gap-2 gradient-bg hover:opacity-90 transition-opacity"
            size="lg"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Generating Summary...
              </>
            ) : (
              <>
                <FiSend className="w-4 h-4" />
                Generate Summary
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {isLoading && <LoadingSkeleton />}
      {!isLoading && result && <ResultDisplay result={result} originalText={text} />}
    </div>
  );
}
