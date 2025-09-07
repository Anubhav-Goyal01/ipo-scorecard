import type { FinancialRow } from "@/lib/types";
import MiniLineChart from "@/components/MiniLineChart";
import { fmtCr } from "@/lib/format";

export default function TrendsCard({ rows }: { rows: FinancialRow[] }) {
  const f = rows || [];
  const fy = f.map((r) => r.fy || "");
  const revenue = f.map((r) => (typeof r.revenue_cr === 'number' ? r.revenue_cr : null));
  const ebitda = f.map((r) => (typeof r.ebitda_cr === 'number' ? r.ebitda_cr : null));
  const pat = f.map((r) => (typeof r.pat_cr === 'number' ? r.pat_cr : null));

  const last = (vals: (number | null)[]) => {
    for (let i = vals.length - 1; i >= 0; i--) if (typeof vals[i] === 'number') return vals[i] as number;
    return null;
  };

  return (
    <section className="w-full max-w-4xl mx-auto p-6 rounded-lg border border-gray-300 bg-white text-gray-900">
      <h2 className="text-lg font-semibold mb-4 text-gray-900">Trends</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex flex-col gap-2">
          <div className="text-sm text-gray-600">Revenue (₹ cr)</div>
          <MiniLineChart values={revenue} />
          <div className="text-xs text-gray-600">Latest: <span className="font-medium text-gray-900">{fmtCr(last(revenue))}</span></div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="text-sm text-gray-600">EBITDA (₹ cr)</div>
          <MiniLineChart values={ebitda} />
          <div className="text-xs text-gray-600">Latest: <span className="font-medium text-gray-900">{fmtCr(last(ebitda))}</span></div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="text-sm text-gray-600">PAT (₹ cr)</div>
          <MiniLineChart values={pat} />
          <div className="text-xs text-gray-600">Latest: <span className="font-medium text-gray-900">{fmtCr(last(pat))}</span></div>
        </div>
      </div>
      <div className="text-xs text-gray-500 mt-3">Each chart shows the trend across reported years; missing data is smoothed.</div>
    </section>
  );
} 