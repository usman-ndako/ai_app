// API Request & Response Types

export type SummaryType = 'standard' | 'executive' | 'legal' | 'technical' | 'financial';

export interface SummaryRequest {
  text: string;
  summary_type: SummaryType;
}

export interface SummaryMetadata {
  summary_type: SummaryType;
  original_length: number;
  summary_length: number;
  compression_ratio: string;
  processing_time_seconds: number;
  model_version: string;
}

export interface SummaryResponse {
  success: boolean;
  summary: string;
  metadata: SummaryMetadata;
}

export interface ApiError {
  detail: string;
}

export interface SummaryTypeConfig {
  value: SummaryType;
  label: string;
  description: string;
  icon: string;
}

// Summary type configurations for UI
export const SUMMARY_TYPES: SummaryTypeConfig[] = [
  {
    value: 'executive',
    label: 'Executive',
    description: 'Strategic C-suite brief focusing on business outcomes',
    icon: '👔'
  },
  {
    value: 'legal',
    label: 'Legal',
    description: 'Precise legal summary with obligations and deadlines',
    icon: '⚖️'
  },
  {
    value: 'technical',
    label: 'Technical',
    description: 'Technical summary focusing on specs and implementations',
    icon: '⚙️'
  },
  {
    value: 'financial',
    label: 'Financial',
    description: 'Financial summary highlighting numbers and metrics',
    icon: '💰'
  },
  {
    value: 'standard',
    label: 'Standard',
    description: 'Balanced general-purpose summary',
    icon: '📄'
  }
];