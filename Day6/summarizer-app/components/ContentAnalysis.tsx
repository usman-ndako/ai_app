import type { ContentAnalysis } from '@/types'; // Add 'type' keyword
import { BarChart3, Lightbulb, Target } from 'lucide-react';

interface ContentAnalysisProps {
  analysis: ContentAnalysis | null;
}

export default function ContentAnalysis({ analysis }: ContentAnalysisProps) {
  if (!analysis) return null;

  const confidenceColors = {
    low: 'text-yellow-600 bg-yellow-100',
    medium: 'text-orange-600 bg-orange-100',
    high: 'text-green-600 bg-green-100',
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="text-blue-500" size={20} />
        <h3 className="text-lg font-semibold">Content Analysis</h3>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{analysis.financial_content}</div>
          <div className="text-sm text-gray-600">Financial Terms</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{analysis.legal_terms}</div>
          <div className="text-sm text-gray-600">Legal Terms</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">{analysis.technical_terms}</div>
          <div className="text-sm text-gray-600">Technical Terms</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">{analysis.business_terms}</div>
          <div className="text-sm text-gray-600">Business Terms</div>
        </div>
      </div>

      {analysis.content_distribution && (
        <div className="space-y-2">
          <h4 className="font-medium text-gray-700">Content Distribution</h4>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full"
              style={{ width: `${analysis.content_distribution.financial}%` }}
            ></div>
            <div
              className="bg-green-600 h-2 rounded-full -mt-2"
              style={{ width: `${analysis.content_distribution.legal}%` }}
            ></div>
            <div
              className="bg-purple-600 h-2 rounded-full -mt-2"
              style={{ width: `${analysis.content_distribution.technical}%` }}
            ></div>
            <div
              className="bg-orange-600 h-2 rounded-full -mt-2"
              style={{ width: `${analysis.content_distribution.business}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-xs text-gray-500">
            <span>Financial: {analysis.content_distribution.financial}%</span>
            <span>Legal: {analysis.content_distribution.legal}%</span>
            <span>Technical: {analysis.content_distribution.technical}%</span>
            <span>Business: {analysis.content_distribution.business}%</span>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between pt-4 border-t">
        <div className="flex items-center gap-2">
          <Lightbulb size={16} className="text-yellow-500" />
          <span className="text-sm font-medium">Recommended:</span>
          <span className="capitalize font-semibold text-blue-600">{analysis.recommended_type}</span>
        </div>
        <div className="flex items-center gap-2">
          <Target size={16} className="text-gray-500" />
          <span className="text-sm font-medium">Confidence:</span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${confidenceColors[analysis.confidence]}`}>
            {analysis.confidence}
          </span>
        </div>
      </div>
    </div>
  );
}