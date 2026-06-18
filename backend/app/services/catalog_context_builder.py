from typing import Any

def build_catalog_context(catalog_rows: list[dict[str, Any]]) -> str:
    """
    Convert catalog rows into compact text context for OpenAI.

    Keep this compact. Do not send the entire database schema.
    Send only rows returned from metadata_search.
    """
    if not catalog_rows:
        return "No catalog metadata available."

    lines: list[str] = []

    for row in catalog_rows:
        line = (
            f"- data_source_id={row.get('data_source_id')}; "
            f"database_type={row.get('database_type')}; "
            f"schema={row.get('schema_name')}; "
            f"table={row.get('table_name')}; "
            f"column={row.get('column_name')}; "
            f"type={row.get('column_type')}; "
            f"business_name={row.get('business_name')}; "
            f"description={row.get('description')}; "
            f"aliases={row.get('aliases')}; "
            f"is_time_column={row.get('is_time_column')}; "
            f"is_value_column={row.get('is_value_column')}; "
            f"is_category_column={row.get('is_category_column')}; "
            f"default_aggregation={row.get('default_aggregation')}; "
            f"default_chart={row.get('default_chart')}"
        )

        lines.append(line)

    return "\n".join(lines)
