import { Toaster } from 'sonner';
import SummarizerForm from '@/components/summarizer-form';
import ApiHealthIndicator from '@/components/api-health-indicator';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Toaster position="top-right" richColors />
      
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gradient-text">AI Document Summarizer</span>
        </h1>
        <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto px-4">
          Transform lengthy documents into concise, context-aware summaries. 
          Choose from 5 professional summary types tailored to your specific needs.
        </p>
          <div className="flex items-center justify-center gap-4 mt-6 flex-wrap">
            <ApiHealthIndicator />
            <div className="text-sm text-slate-500">
              • 5 Summary Types • Fact-Grounded • Enterprise-Ready
            </div>
          </div>
        </div>

        {/* Main Summarizer Component */}
        <SummarizerForm />

        {/* Features Section */}
        <div className="mt-16 grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="text-center p-6">
            <div className="text-4xl mb-3">⚡</div>
            <h3 className="font-semibold mb-2">Lightning Fast</h3>
            <p className="text-sm text-slate-600">
              Process documents in seconds with optimized AI models
            </p>
          </div>
          <div className="text-center p-6">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="font-semibold mb-2">Context-Aware</h3>
            <p className="text-sm text-slate-600">
              Each summary type uses appropriate tone and focus
            </p>
          </div>
          <div className="text-center p-6">
            <div className="text-4xl mb-3">🔒</div>
            <h3 className="font-semibold mb-2">Fact-Grounded</h3>
            <p className="text-sm text-slate-600">
              AI strictly uses only information from your document
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}