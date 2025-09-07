"use client";

import { useState } from "react";
import UploadBox from "@/components/UploadBox";
import TermsCard from "@/components/TermsCard";
import FinancialsTable from "@/components/FinancialsTable";
import MetricsCard from "@/components/MetricsCard";
import VerdictCard from "@/components/VerdictCard";
import TrendsCard from "@/components/TrendsCard";
import type { AnalyzeResponse, FinancialQualityBlock, TermsAndFinancialsBlock, VerdictBlock } from "@/lib/types";

export default function Home() {
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const taf = data?.components.find((b) => b.component === "terms_and_financials") as TermsAndFinancialsBlock | undefined;
  const fq = data?.components.find((b) => b.component === "financial_quality") as FinancialQualityBlock | undefined;
  const vd = data?.components.find((b) => b.component === "verdict") as VerdictBlock | undefined;

  const resetUpload = () => {
    setData(null);
    setFileName(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <header className="border-b border-gray-300 bg-white">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-base font-semibold tracking-tight">IPO Scorecard</h1>
          {data ? (
            <div className="flex items-center gap-3 text-xs text-gray-700">
              <span className="truncate max-w-[240px]">Current PDF: <span className="font-medium text-gray-900" title={fileName || undefined}>{fileName || "—"}</span></span>
              <button
                type="button"
                onClick={resetUpload}
                className="px-2 py-1 border border-gray-400 rounded bg-white text-gray-900 hover:bg-gray-100"
              >
                Upload another PDF
              </button>
            </div>
          ) : (
            <div className="text-xs text-gray-500"></div>
          )}
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 flex flex-col gap-6">
        {!data && <UploadBox onResult={setData} onSelectedFileName={setFileName} />}

        {!data && (
          <section className="flex items-center justify-center h-[50vh] text-sm text-gray-500">
            Upload a DRHP/RHP PDF to get started.
          </section>
        )}

        {taf && (
          <TermsCard company={taf.company} terms={taf.terms} />
        )}

        {taf && taf.financials?.length > 0 && (
          <>
            <FinancialsTable rows={taf.financials} />
            <TrendsCard rows={taf.financials} />
          </>
        )}

        {fq && (
          <MetricsCard metrics={fq.metrics} />
        )}

        {vd && (
          <VerdictCard block={vd} />
        )}

      </main>

      <footer className="border-t border-gray-300 bg-white mt-10">
        <div className="max-w-5xl mx-auto px-6 py-4 text-xs text-gray-500">
        </div>
      </footer>
    </div>
  );
}
