export type QueryIntent =
  | "trend"
  | "summary"
  | "compare"
  | "raw_table"
  | "downtime";

export interface QueryPlan {
  intent: QueryIntent;
  database_type: string | null;
  data_source_id: number | null;
  schema_name: string | null;
  table_name: string | null;
  time_column: string | null;
  value_column: string | null;
  category_column: string | null;
  status_column: string | null;
  start_time: string | null;
  end_time: string | null;
  aggregation: string | null;
  group_by: string | null;
  limit: number | null;
  chart_type: string | null;
  explanation?: string | null;
}

export interface ChatResponse {
  answer: string;
  prompt: string;
  planner_source: string;
  plan: QueryPlan;
  sql: string;
  params: Record<string, unknown>;
  rows: Record<string, unknown>[];
  chart: {
    chart_library: string;
    option: Record<string, unknown>;
  };
  // New fields for clarification flow
  status?: string; // e.g., "success", "needs_clarification"
  question?: string; // clarification question when status is "needs_clarification"
}
