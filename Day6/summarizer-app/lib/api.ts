import { SummaryRequest, SummaryResponse, ContentAnalysis, SummaryTypes } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiService = {
  async summarize(text: string, summaryType: SummaryRequest['summary_type']): Promise<SummaryResponse> {
    const response = await fetch(`${API_BASE_URL}/summarize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        summary_type: summaryType,
      } as SummaryRequest),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate summary');
    }

    return response.json();
  },

  async analyzeContent(text: string): Promise<ContentAnalysis> {
    const response = await fetch(`${API_BASE_URL}/analyze-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error('Failed to analyze content');
    }

    return response.json();
  },

  async getSummaryTypes(): Promise<SummaryTypes> {
    const response = await fetch(`${API_BASE_URL}/summary-types`);
    if (!response.ok) {
      throw new Error('Failed to fetch summary types');
    }
    return response.json();
  },

  async healthCheck(): Promise<boolean> {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  },
};