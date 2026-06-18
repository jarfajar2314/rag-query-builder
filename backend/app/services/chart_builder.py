from typing import Any

def build_chart_config(plan: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Converts query results into an ECharts configuration object or other UI hints.
    Supports trend, compare, summary, raw_table, and downtime intents.
    """
    chart_type = plan.get("chart_type")
    
    if chart_type == "line":
        x_data = [str(row["time_bucket"]) for row in rows]
        y_data = [float(row["value"]) if row["value"] is not None else 0 for row in rows]
        
        return {
            "chart_library": "echarts",
            "option": {
                "title": {"text": f"{plan.get('value_column', 'Value').capitalize()} Trend"},
                "tooltip": {"trigger": "axis"},
                "xAxis": {"type": "category", "data": x_data},
                "yAxis": {"type": "value"},
                "series": [{"name": plan.get("value_column", "value"), "type": "line", "data": y_data}]
            }
        }
        
    elif chart_type == "bar":
        x_data = [str(row.get("category", "Unknown")) for row in rows]
        y_data = [float(row["value"]) if row["value"] is not None else 0 for row in rows]
        
        return {
            "chart_library": "echarts",
            "option": {
                "title": {"text": "Comparison"},
                "tooltip": {"trigger": "axis"},
                "xAxis": {"type": "category", "data": x_data},
                "yAxis": {"type": "value"},
                "series": [{"name": plan.get("value_column", "value"), "type": "bar", "data": y_data}]
            }
        }
        
    elif chart_type == "kpi":
        value = rows[0]["value"] if rows else 0
        return {
            "chart_library": "kpi_card",
            "option": {
                "title": f"Total {plan.get('value_column', 'Value')}",
                "value": float(value) if value is not None else 0
            }
        }
        
    elif chart_type == "table":
        return {
            "chart_library": "data_table",
            "option": {
                "columns": list(rows[0].keys()) if rows else [],
            }
        }
        
    elif chart_type == "timeline":
        return {
            "chart_library": "timeline",
            "option": {
                "title": "Downtime Timeline"
            }
        }
        
    return {}
