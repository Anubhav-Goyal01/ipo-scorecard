import { ReactNode } from "react";

export default function InfoTip({ label, children }: { label: string; children: ReactNode }) {
  return (
    <span className="relative inline-block group align-middle">
      <button
        type="button"
        tabIndex={0}
        aria-label={label}
        className="inline-flex items-center justify-center w-4 h-4 rounded-full border border-gray-400 text-gray-700 text-[10px] leading-none cursor-help focus:outline-none bg-white"
      >
        i
      </button>
      <span className="absolute left-0 top-full mt-2 hidden group-hover:block group-focus-within:block z-10 w-64 p-2 text-xs rounded-md border border-gray-300 bg-white text-gray-800 shadow-sm">
        <strong className="block mb-1 text-gray-900">{label}</strong>
        <span className="text-gray-700">{children}</span>
      </span>
    </span>
  );
} 