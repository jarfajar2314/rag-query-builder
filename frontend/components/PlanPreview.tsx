import { useState } from "react";
import { QueryPlan } from "@/types/chat";

interface PlanPreviewProps {
  plan: QueryPlan;
  source: string;
}

export function PlanPreview({ plan, source }: PlanPreviewProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden my-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 flex justify-between items-center transition-colors text-sm font-semibold text-gray-700"
      >
        <span>🧠 Query Plan (Source: {source})</span>
        <span className="text-xs text-gray-500">{isOpen ? "Hide" : "Show"}</span>
      </button>

      {isOpen && (
        <div className="p-4 bg-gray-900 text-green-400 font-mono text-sm overflow-x-auto">
          <pre>
            <code>{JSON.stringify(plan, null, 2)}</code>
          </pre>
        </div>
      )}
    </div>
  );
}
