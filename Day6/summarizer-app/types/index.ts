export interface SummaryRequest {
  text: string;
  summary_type: 'standard' | 'executive' | 'legal' | 'technical' | 'financial';
}

export interface SummaryResponse {
  success: boolean;
  summary: string;
  metadata: {
    summary_type: string;
    model: string;
    original_length: number;
    summary_length: number;
    processing_time_seconds: number;
    technique: string;
  };
}

export interface ContentAnalysis {
  financial_content: number;
  legal_terms: number;
  technical_terms: number;
  business_terms: number;
  recommended_type: string;
  confidence: 'low' | 'medium' | 'high';
  content_distribution: {
    financial: number;
    legal: number;
    technical: number;
    business: number;
  };
}

export interface SummaryType {
  description: string;
  model: string;
}

export interface SummaryTypes {
  [key: string]: SummaryType;
}

export type ApiStatus = 'checking' | 'online' | 'offline';