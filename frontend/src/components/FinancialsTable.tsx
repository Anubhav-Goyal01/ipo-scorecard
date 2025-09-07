import type { FinancialRow } from "@/lib/types";
import { fmtCr } from "@/lib/format";

export default function FinancialsTable({ rows }: { rows: FinancialRow[] }) {
  return (
    <section className="w-full max-w-4xl mx-auto p-6 rounded-lg border border-gray-300 bg-white text-gray-900">
      <h2 className="text-lg font-semibold mb-4 text-gray-900">Financial Summary (₹ crore)</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-600 border-b border-gray-200">
              <th className="py-2 pr-4">FY</th>
              <th className="py-2 pr-4">Revenue</th>
              <th className="py-2 pr-4">EBITDA</th>
              <th className="py-2 pr-4">PAT</th>
              <th className="py-2 pr-4">Net Worth</th>
              <th className="py-2 pr-4">Debt</th>
              <th className="py-2 pr-4">CFO</th>
            </tr>
          </thead>
          <tbody>
            {rows?.map((r, i) => (
              <tr key={i} className="border-b border-gray-100">
                <td className="py-2 pr-4 font-medium text-gray-900">{r.fy || "—"}</td>
                <td className="py-2 pr-4">{fmtCr(r.revenue_cr as any)}</td>
                <td className="py-2 pr-4">{fmtCr(r.ebitda_cr as any)}</td>
                <td className="py-2 pr-4">{fmtCr(r.pat_cr as any)}</td>
                <td className="py-2 pr-4">{fmtCr(r.networth_cr as any)}</td>
                <td className="py-2 pr-4">{fmtCr(r.debt_cr as any)}</td>
                <td className="py-2 pr-4">{fmtCr(r.cfo_cr as any)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-gray-500">Numbers normalized to ₹ crore with 2 decimals where available.</p>
    </section>
  );
} 