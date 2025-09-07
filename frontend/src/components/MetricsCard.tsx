import type { Metrics } from "@/lib/types";
import { fmtCr, fmtPct } from "@/lib/format";
import InfoTip from "@/components/InfoTip";

export default function MetricsCard({ metrics }: { metrics: Metrics }) {
  return (
    <section className="w-full max-w-4xl mx-auto p-6 rounded-lg border border-gray-300 bg-white text-gray-900">
      <h2 className="text-lg font-semibold mb-4 text-gray-900">Financial Quality</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
        <div>
          <div className="text-gray-500">Window (years)</div>
          <div className="font-medium">{metrics.window_years || "—"}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">Revenue CAGR <InfoTip label="Revenue CAGR">Average annual growth in revenue across the reported years.</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.revenue_cagr)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">PAT CAGR <InfoTip label="PAT CAGR">Average annual growth in profit after tax.</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.pat_cagr)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">EBITDA CAGR <InfoTip label="EBITDA CAGR">Average annual growth in operating profit before depreciation and interest.</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.ebitda_cagr)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">PAT Margin (latest) <InfoTip label="PAT Margin">Profit after tax as a share of revenue in the latest year.</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.pat_margin)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">EBITDA Margin (latest) <InfoTip label="EBITDA Margin">Operating profit as a share of revenue in the latest year.</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.ebitda_margin)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">EBITDA Margin Trend <InfoTip label="Margin Trend">Change in EBITDA margin from first to last reported year.</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.margin_trend_ebitda)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">Revenue Volatility <InfoTip label="Volatility">How bumpy revenue growth is year to year (lower is steadier).</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.revenue_volatility)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">Debt / Net Worth <InfoTip label="Leverage">Higher values mean more borrowing compared to equity.</InfoTip></div>
          <div className="font-medium">{typeof metrics.debt_to_networth === 'number' ? metrics.debt_to_networth.toFixed(2) : "—"}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">Net Debt / EBITDA <InfoTip label="Debt to Profit">How many years of operating profit to repay net debt (lower is better).</InfoTip></div>
          <div className="font-medium">{typeof metrics.net_debt_to_ebitda === 'number' ? metrics.net_debt_to_ebitda.toFixed(2) : "—"}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">CFO (latest) <InfoTip label="Cash from Operations">Cash generated from core business in the latest year.</InfoTip></div>
          <div className="font-medium">{fmtCr(metrics.cfo_latest)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">CFO / PAT <InfoTip label="Cash Conversion">How much profit converts to cash (closer to 100% is better).</InfoTip></div>
          <div className="font-medium">{fmtPct(metrics.cfo_to_pat)}</div>
        </div>
        <div>
          <div className="text-gray-500 flex items-center gap-1">Years with +CFO <InfoTip label="Consistency">Share of reported years with positive cash flow from operations.</InfoTip></div>
          <div className="font-medium">{typeof metrics.cfo_positive_years_ratio === 'number' ? `${Math.round(metrics.cfo_positive_years_ratio * 100)}%` : "—"}</div>
        </div>
      </div>
      <p className="mt-3 text-xs text-gray-500">Higher growth and margins are better. Positive and consistent cash flows strengthen conviction; lower leverage is safer.</p>
    </section>
  );
} 