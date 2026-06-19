"use client";

import { useState } from "react";
import { sendChatPrompt } from "@/lib/api";
import { ChatResponse } from "@/types/chat";
import { ChartRenderer } from "@/components/ChartRenderer";
import { DataTable } from "@/components/DataTable";
import { SqlPreview } from "@/components/SqlPreview";
import { PlanPreview } from "@/components/PlanPreview";

export default function Home() {
	const [prompt, setPrompt] = useState("");
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [response, setResponse] = useState<ChatResponse | null>(null);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!prompt.trim()) return;

		setLoading(true);
		setError(null);

		try {
			const result = await sendChatPrompt(prompt);
			setResponse(result);
		} catch (err: any) {
			setError(err.message || "An unexpected error occurred.");
		} finally {
			setLoading(false);
		}
	};

	return (
		<main className="min-h-screen bg-gray-50 text-gray-900 p-8 font-sans">
			<div className="max-w-5xl mx-auto space-y-8">
				{/* Header */}
				<div className="text-center">
					<h1 className="text-4xl font-extrabold tracking-tight text-blue-700 mb-2">
						RAG Query Builder
					</h1>
					<p className="text-gray-500">
						Ask natural language questions about your database
					</p>
				</div>

				{/* Input Form */}
				<form onSubmit={handleSubmit} className="relative">
					<div className="overflow-hidden rounded-lg border border-gray-300 shadow-sm focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
						<label htmlFor="prompt" className="sr-only">
							Prompt
						</label>
						<textarea
							id="prompt"
							name="prompt"
							rows={3}
							className="block w-full resize-none border-0 py-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-lg sm:leading-6 px-4"
							placeholder="e.g. compare sales by region this month..."
							value={prompt}
							onChange={(e) => setPrompt(e.target.value)}
							onKeyDown={(e) => {
								if (e.key === "Enter" && !e.shiftKey) {
									e.preventDefault();
									handleSubmit(e);
								}
							}}
						/>
					</div>
					<div className="absolute inset-y-0 right-0 flex py-1.5 pr-1.5">
						<button
							type="submit"
							disabled={loading || !prompt.trim()}
							className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50 disabled:cursor-not-allowed m-2 transition-colors"
						>
							{loading ? (
								<svg
									className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
								>
									<circle
										className="opacity-25"
										cx="12"
										cy="12"
										r="10"
										stroke="currentColor"
										strokeWidth="4"
									></circle>
									<path
										className="opacity-75"
										fill="currentColor"
										d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
									></path>
								</svg>
							) : (
								"Ask"
							)}
						</button>
					</div>
				</form>

				{/* Error State */}
				{error && (
					<div className="rounded-md bg-red-50 p-4 border border-red-200">
						<div className="flex">
							<div className="ml-3">
								<h3 className="text-sm font-medium text-red-800">
									Error
								</h3>
								<div className="mt-2 text-sm text-red-700">
									<p>{error}</p>
								</div>
							</div>
						</div>
					</div>
				)}

				{/* Results */}
				{response && (
					<div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
						{/* Answer Card */}
						<div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
							<h2 className="text-lg font-semibold text-gray-800 mb-2">
								Answer
							</h2>
							<p className="text-gray-600">{response.answer}</p>
						</div>

						{/* Chart (if exists) */}
						{response.chart &&
							Object.keys(response.chart).length > 0 &&
							response.chart.option && (
								<ChartRenderer option={response.chart.option} />
							)}

						{/* Data Table */}
						{response.rows && response.rows.length > 0 && (
							<div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
								<h2 className="text-lg font-semibold text-gray-800 mb-4">
									Data
								</h2>
								<DataTable rows={response.rows} />
							</div>
						)}

						{/* Debugging section */}
						<div className="pt-8">
							<h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4 border-b border-gray-200 pb-2">
								Developer Tools
							</h3>
							<PlanPreview
								plan={response.plan}
								source={response.planner_source}
							/>
							<SqlPreview
								sql={response.sql}
								params={response.params}
							/>
						</div>
					</div>
				)}
			</div>
		</main>
	);
}
