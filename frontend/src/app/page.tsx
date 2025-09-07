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
  const taf = data?.components.find((b) => b.component === "terms_and_financials") as TermsAndFinancialsBlock | undefined;
  const fq = data?.components.find((b) => b.component === "financial_quality") as FinancialQualityBlock | undefined;
  const vd = data?.components.find((b) => b.component === "verdict") as VerdictBlock | undefined;

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <header className="border-b border-gray-300 bg-white">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-base font-semibold tracking-tight">IPO Scorecard</h1>
          <div className="text-xs text-gray-500"></div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 flex flex-col gap-6">
        <UploadBox onResult={setData} />

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
