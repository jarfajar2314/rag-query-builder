"use client";

import dynamic from "next/dynamic";

const ReactECharts = dynamic(() => import("echarts-for-react"), { ssr: false });

interface ChartRendererProps {
  option: Record<string, unknown>;
}

export function ChartRenderer({ option }: ChartRendererProps) {
  // If it's a simple KPI chart, render a special card instead of ECharts
  if (option.title && typeof option.title === 'string' && option.title.startsWith("Total ") && typeof option.value !== 'undefined') {
      return (
          <div className="p-6 bg-white rounded-lg shadow-md border border-gray-100 flex flex-col items-center justify-center min-h-[200px]">
              <h3 className="text-lg text-gray-500 font-medium mb-2">{option.title}</h3>
              <p className="text-4xl font-bold text-blue-600">{option.value as number}</p>
          </div>
      );
  }

  return (
    <div className="w-full h-[400px] p-4 bg-white rounded-lg shadow-sm border border-gray-100">
      <ReactECharts option={option} style={{ height: "100%", width: "100%" }} />
    </div>
  );
}
