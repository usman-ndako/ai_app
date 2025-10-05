'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function Home() {
  const [streamlitUrl] = useState('http://localhost:8501');
  const [iframeHeight, setIframeHeight] = useState(800);

  // Dynamically resize iframe to viewport
  useEffect(() => {
    const updateHeight = () => setIframeHeight(window.innerHeight - 200);
    updateHeight();
    window.addEventListener('resize', updateHeight);
    return () => window.removeEventListener('resize', updateHeight);
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">
            🚀 Business KPI Dashboard
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Interactive AI-powered insights — Upload data, analyze trends, and forecast futures with one click.
          </p>
        </header>

        {/* Dashboard Iframe */}
        <section className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <h2 className="text-xl font-bold">Dashboard View</h2>
            <p className="text-blue-100 text-sm">Interactive analytics — optimized for all devices</p>
          </div>

          <iframe
            src={streamlitUrl}
            width="100%"
            height={iframeHeight}
            className="border-0 w-full"
            title="KPI Dashboard"
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-downloads"
            loading="lazy"
          />
        </section>

        {/* Footer */}
        <footer className="text-center mt-12 text-sm text-gray-500">
          <p>© 2025 AI Entrepreneur Intensive | Built with ❤️ for Phase 2</p>
        </footer>
      </div>
    </main>
  );
}
