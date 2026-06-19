interface DataTableProps {
  rows: Record<string, unknown>[];
}

export function DataTable({ rows }: DataTableProps) {
  if (rows.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 bg-gray-50 rounded-lg">
        No data returned.
      </div>
    );
  }

  const columns = Object.keys(rows[0]);

  return (
    <div className="w-full overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-gray-50 transition-colors">
              {columns.map((column) => (
                <td
                  key={`${rowIndex}-${column}`}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
                >
                  {String(row[column] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
