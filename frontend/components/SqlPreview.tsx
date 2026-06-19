import { useState } from "react";

interface SqlPreviewProps {
  sql: string;
  params: Record<string, unknown>;
}

export function SqlPreview({ sql, params }: SqlPreviewProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (!sql) return null;

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden my-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 flex justify-between items-center transition-colors text-sm font-semibold text-gray-700"
      >
        <span>🔍 Generated SQL</span>
        <span className="text-xs text-gray-500">{isOpen ? "Hide" : "Show"}</span>
      </button>

      {isOpen && (
        <div className="p-4 bg-gray-900 text-gray-100 font-mono text-sm overflow-x-auto">
          <pre>
            <code>{sql.trim()}</code>
          </pre>
          {Object.keys(params).length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-700">
              <h4 className="text-gray-400 mb-2">Parameters:</h4>
              <pre className="text-green-400">
                <code>{JSON.stringify(params, null, 2)}</code>
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
