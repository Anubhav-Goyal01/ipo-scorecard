import type { Terms } from "@/lib/types";
import { fmtDate, fmtInt } from "@/lib/format";

export default function TermsCard({ company, terms }: { company: string | null; terms: Terms }) {
  return (
    <section className="w-full max-w-4xl mx-auto p-6 rounded-lg border border-gray-300 bg-white text-gray-900">
      <h2 className="text-lg font-semibold mb-4 text-gray-900">IPO Snapshot</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
        <div>
          <div className="text-gray-500">Company</div>
          <div className="font-medium">{company || "—"}</div>
        </div>
        <div>
          <div className="text-gray-500">Price Band</div>
          <div className="font-medium">
            {Array.isArray(terms.price_band) ? terms.price_band.join(" – ") : "—"}
          </div>
        </div>
        <div>
          <div className="text-gray-500">Lot Size (shares)</div>
          <div className="font-medium">{fmtInt(terms.lot_size)}</div>
        </div>
        <div>
          <div className="text-gray-500">Open Date</div>
          <div className="font-medium">{fmtDate(terms.open_date)}</div>
        </div>
        <div>
          <div className="text-gray-500">Close Date</div>
          <div className="font-medium">{fmtDate(terms.close_date)}</div>
        </div>
      </div>
    </section>
  );
} 