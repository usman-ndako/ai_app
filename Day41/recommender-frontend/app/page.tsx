"use client";
import { useState } from "react";

type Recommendation = {
  item_id: number;
  title: string;
  category: string;
  price: number;
  margin: number;
};

export default function Home() {
  const [userId, setUserId] = useState<string>("");
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  const fetchRecommendations = async () => {
    if (!userId) return;
    setLoading(true);
    setRecs([]);
    try {
      const url = `${backendUrl}/recommend/?user_id=${userId}&n=5`;
      const response = await fetch(url);
      const data = await response.json();
      setRecs(data.recommendations || []);
    } catch (err) {
      setRecs([]);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen w-full flex flex-col items-center justify-center bg-gradient-to-br from-[#ede9fe] via-[#f3f4f6] to-[#c7d2fe] relative font-sans">
      {/* Decorative background shapes */}
      <div className="absolute top-0 left-0 right-0 h-32 bg-gradient-to-tr from-[#7c3aed77] via-[#c4b5fd33] to-[#818cf877] blur-lg -z-10"/>
      <div className="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-bl from-[#7c3aed44] to-[#c4b5fd22] rounded-full blur-2xl -z-10"/>
      
      <div className="w-full max-w-md mx-auto p-4 my-8">
        <div className="bg-white/60 backdrop-blur-lg shadow-2xl rounded-3xl border border-[#b4b4c9] px-6 py-10 flex flex-col items-center gap-6 animate-fade-in">
          <h1 className="text-3xl md:text-4xl font-extrabold text-[#7c3aed] mb-1 text-center tracking-tight drop-shadow-sm">
            AI Product Recommender
          </h1>
          <p className="mb-2 text-gray-500 text-sm text-center font-medium">
            Enter your user ID to unlock your top personalized picks
          </p>
          <div className="flex w-full gap-2 items-center justify-center">
            <input
              type="number"
              value={userId}
              placeholder="User ID"
              onChange={e => setUserId(e.target.value)}
              min={1}
              className="w-28 px-3 py-2 rounded-lg border border-[#ddd] focus:outline-none focus:ring-2 focus:ring-[#7c3aed] bg-white/80 shadow"
            />
            <button
              className={`transition-all duration-200 font-semibold px-6 py-2 rounded-lg shadow
                ${loading || !userId ? 'bg-[#ddd] text-gray-400 cursor-not-allowed' : 'bg-[#7c3aed] text-white hover:bg-[#6e34c5]'}`}
              onClick={fetchRecommendations}
              disabled={loading || !userId}
              style={{background: loading || !userId ? '#ddd' : 'var(--color-primary)'}}
            >
              {loading ? "Loading..." : "Show My Picks"}
            </button>
          </div>
          <div className="w-full mt-4">
            {recs.length > 0 && (
              <ul className="space-y-4 mt-4">
                {recs.map(rec => (
                  <li
                    key={rec.item_id}
                    className="flex flex-col md:flex-row md:items-center md:justify-between bg-gradient-to-r from-[#fafafa] via-[#f3e8ff] to-[#ede9fe] border-l-4 border-[#7c3aed] rounded-xl shadow px-4 py-3 animate-fade-in"
                  >
                    <div>
                      <span className="font-bold text-[#7c3aed] text-lg">{rec.title}</span>
                      <span className="ml-2 text-xs text-[#6d28d9] font-medium">(Category: {rec.category})</span>
                    </div>
                    <div className="flex flex-wrap gap-4 mt-1 md:mt-0 text-sm">
                      <span className="text-green-700 font-semibold">₦{rec.price}</span>
                      <span className="text-[#a78bfa]">Margin: ₦{rec.margin}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
            {!loading && recs.length === 0 && userId && (
              <p className="mt-10 text-[#b4b4c9] text-center text-base font-semibold">No recommendations found for this user.</p>
            )}
          </div>
        </div>
        {/* Portfolio note area */}
        <p className="mt-10 mb-2 text-center text-sm text-gray-400">Built with Next.js, FastAPI and Tailwind CSS. <br />AI-powered recommendation engine for business portfolios.</p>
      </div>
    </main>
  );
}
