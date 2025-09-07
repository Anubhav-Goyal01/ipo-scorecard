type Point = { x: number; y: number };

function normalize(values: (number | null | undefined)[]): number[] {
  const nums = values.map((v) => (typeof v === "number" && isFinite(v) ? v : NaN));
  const clean = nums.filter((n) => !isNaN(n));
  if (clean.length === 0) return values.map(() => 0.5);
  const min = Math.min(...clean);
  const max = Math.max(...clean);
  if (min === max) return values.map(() => 0.5);
  return values.map((v) => (typeof v === "number" && isFinite(v) ? (v - min) / (max - min) : 0.5));
}

export default function MiniLineChart({ values, height = 60 }: { values: (number | null | undefined)[]; height?: number }) {
  const n = values.length || 0;
  const norm = normalize(values);
  const w = Math.max(120, n * 30);
  const h = height;
  const pts: Point[] = norm.map((v, i) => ({ x: (i / Math.max(1, n - 1)) * (w - 20) + 10, y: (1 - v) * (h - 20) + 10 }));
  const d = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ");

  return (
    <svg width={w} height={h} className="text-gray-800">
      <rect x={0} y={0} width={w} height={h} rx={8} className="fill-white stroke-gray-300" />
      {pts.length > 1 && (
        <path d={d} className="stroke-gray-800 fill-none" strokeWidth={2} />
      )}
      {pts.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r={2} className="fill-gray-800" />
      ))}
    </svg>
  );
} 