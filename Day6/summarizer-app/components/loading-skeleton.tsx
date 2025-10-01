export default function LoadingSkeleton() {
  return (
    <div className="space-y-4 animate-pulse">
      {/* Summary Card Skeleton */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-lg p-6 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-slate-200 rounded-full"></div>
          <div className="space-y-2 flex-1">
            <div className="h-5 bg-slate-200 rounded w-1/4"></div>
            <div className="h-4 bg-slate-200 rounded w-1/2"></div>
          </div>
        </div>
        <div className="space-y-3 mt-4">
          <div className="h-4 bg-slate-200 rounded"></div>
          <div className="h-4 bg-slate-200 rounded"></div>
          <div className="h-4 bg-slate-200 rounded w-5/6"></div>
        </div>
      </div>

      {/* Metrics Card Skeleton */}
      <div className="bg-white rounded-lg border border-slate-200 shadow-lg p-6">
        <div className="h-5 bg-slate-200 rounded w-1/4 mb-4"></div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="p-4 bg-slate-50 rounded-lg space-y-2">
              <div className="h-4 bg-slate-200 rounded w-3/4"></div>
              <div className="h-6 bg-slate-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}