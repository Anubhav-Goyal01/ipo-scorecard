import type { VerdictBlock } from "@/lib/types";

export default function VerdictCard({ block }: { block: VerdictBlock }) {
  const tone = block.verdict === "Apply" ? "bg-gray-900 text-white" : block.verdict === "Neutral" ? "bg-gray-700 text-white" : "bg-white text-gray-900 border border-gray-400";
  return (
    <section className={`w-full max-w-4xl mx-auto p-6 rounded-lg ${tone}`}>
      <h2 className="text-lg font-semibold mb-3">Verdict</h2>
      <div className="text-sm flex flex-col gap-2">
        <div className="flex items-center gap-3">
          <span className="font-medium">Recommendation:</span>
          <span className="px-2 py-0.5 rounded-md border border-current text-xs uppercase tracking-wide">{block.verdict}</span>
        </div>
        <div className="flex items-center gap-6">
          <div>
            <div className="opacity-80 text-xs">Score</div>
            <div className="font-medium">{block as any && (block as any).score ? (block as any).score : "—"}</div>
          </div>
          <div>
            <div className="opacity-80 text-xs">Confidence</div>
            <div className="font-medium">{Math.round(block.confidence * 100)}%</div>
          </div>
        </div>
        {block.plain_english && (
          <p className="opacity-90">
            {block.plain_english}
          </p>
        )}
        <ul className="list-disc pl-5 opacity-90">
          {block.why?.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>
    </section>
  );
} 