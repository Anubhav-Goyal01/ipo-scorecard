"use client";

import { useState } from "react";
import { analyzePdf } from "@/lib/api";
import type { AnalyzeResponse } from "@/lib/types";

export default function UploadBox({ onResult, onSelectedFileName }: { onResult: (r: AnalyzeResponse) => void; onSelectedFileName?: (name: string) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }
    try {
      setLoading(true);
      const res = await analyzePdf(file);
      onResult(res);
    } catch (err: any) {
      setError(err?.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleFile = (f: File | null) => {
    setFile(f);
    if (f && onSelectedFileName) onSelectedFileName(f.name);
  };

  return (
    <form onSubmit={onSubmit} className="w-full max-w-2xl mx-auto p-6 rounded-lg border border-gray-300 bg-white text-gray-900">
      <div className="flex flex-col gap-4">
        <label className="text-sm font-medium text-gray-700">Upload IPO PDF (DRHP/RHP)</label>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => handleFile(e.target.files?.[0] || null)}
          className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200"
        />
        {file && (
          <p className="text-xs text-gray-600">Selected: {file.name}</p>
        )}
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center rounded-md border border-gray-400 bg-gray-900 text-white px-4 py-2 text-sm disabled:opacity-60"
        >
          {loading ? "Analyzing…" : "Analyze PDF"}
        </button>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>
    </form>
  );
} 