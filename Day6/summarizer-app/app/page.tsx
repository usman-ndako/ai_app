// app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { apiService } from '@/lib/api';
import type { SummaryTypes, ContentAnalysis, SummaryResponse, ApiStatus } from '@/types';
import SummaryTypeSelector from '@/components/SummaryTypeSelector';
import TextInput from '@/components/TextInput';
import SummaryOutput from '@/components/SummaryOutput';
import ContentAnalysisComponent from '@/components/ContentAnalysis';
import StatusIndicator from '@/components/StatusIndicator';
import { FileText, Zap, Brain } from 'lucide-react';

export default function HomePage() { // Changed from 'Home' to 'HomePage'
  const [text, setText] = useState<string>('');
  const [summaryType, setSummaryType] = useState<string>('standard');
  const [summaryTypes, setSummaryTypes] = useState<SummaryTypes>({});
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [analysis, setAnalysis] = useState<ContentAnalysis | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [apiStatus, setApiStatus] = useState<ApiStatus>('checking');

  useEffect(() => {
    checkApiStatus();
    loadSummaryTypes();
  }, []);

  const checkApiStatus = async () => {
    try {
      const isHealthy = await apiService.healthCheck();
      setApiStatus(isHealthy ? 'online' : 'offline');
    } catch {
      setApiStatus('offline');
    }
  };

  const loadSummaryTypes = async () => {
    try {
      const types = await apiService.getSummaryTypes();
      setSummaryTypes(types);
    } catch (error) {
      console.error('Failed to load summary types:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setAnalyzing(true);
    try {
      const analysisResult = await apiService.analyzeContent(text);
      setAnalysis(analysisResult);
      
      if (analysisResult.confidence !== 'low') {
        setSummaryType(analysisResult.recommended_type);
      }
    } catch (error) {
      alert('Analysis failed: ' + (error as Error).message);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSummarize = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setSummary(null);
    try {
      const result = await apiService.summarize(
        text, 
        summaryType as 'standard' | 'executive' | 'legal' | 'technical' | 'financial'
      );
      setSummary(result);
    } catch (error) {
      alert('Summary generation failed: ' + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-blue-500 rounded-xl">
              <FileText className="text-white" size={32} />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">AI Document Summarizer</h1>
          </div>
          <p className="text-xl text-gray-600 mb-4 max-w-2xl mx-auto">
            Transform lengthy documents into concise, specialized summaries with advanced AI
          </p>
          <StatusIndicator status={apiStatus} />
        </div>

        <div className="max-w-6xl mx-auto space-y-8">
          {/* Summary Type Selection */}
          {Object.keys(summaryTypes).length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Zap className="text-blue-500" size={20} />
                <h2 className="text-2xl font-semibold text-gray-900">Choose Summary Type</h2>
              </div>
              <SummaryTypeSelector
                summaryTypes={summaryTypes}
                selectedType={summaryType}
                onTypeSelect={setSummaryType}
              />
            </div>
          )}

          {/* Text Input */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <TextInput
              value={text}
              onChange={setText}
              onAnalyze={handleAnalyze}
              analyzing={analyzing}
            />
          </div>

          {/* Content Analysis */}
          {analysis && <ContentAnalysisComponent analysis={analysis} />}

          {/* Generate Button */}
          {text.trim() && (
            <div className="text-center">
              <button
                onClick={handleSummarize}
                disabled={loading || apiStatus !== 'online'}
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold text-lg hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating Summary...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <Brain size={20} />
                    Generate {summaryType} Summary
                  </div>
                )}
              </button>
            </div>
          )}

          {/* Summary Output */}
          <SummaryOutput summary={summary} loading={loading} />
        </div>
      </div>
    </div>
  );
}