from typing import Any
from app.db.postgres import get_postgres_connection

def build_catalog_context(catalog_rows: list[dict[str, Any]]) -> str:
    """
    Convert catalog rows into compact text context for OpenAI.

    Keep this compact. Do not send the entire database schema.
    Send only rows returned from metadata_search.
    """
    if not catalog_rows:
        return "No catalog metadata available."

    lines: list[str] = ["## Data Catalog Metadata"]

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

    # Fetch status rules for matched tables
    catalog_ids = [row["id"] for row in catalog_rows if "id" in row]
    
    # We find rules where the status_column, time_column, or category_column is in our matched catalog_rows
    # To keep it simple, we can just load rules where status_column_catalog_id is in catalog_ids.
    if catalog_ids:
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    # Select rules that relate to the columns
                    format_strings = ','.join(['%s'] * len(catalog_ids))
                    cur.execute(f"""
                        SELECT 
                            sr.id, sr.name, sr.description, 
                            dc_stat.data_source_id, dc_stat.schema_name, dc_stat.table_name,
                            dc_time.column_name as time_column,
                            dc_stat.column_name as status_column,
                            dc_cat.column_name as category_column
                        FROM status_rules sr
                        JOIN data_catalog dc_stat ON sr.status_column_catalog_id = dc_stat.id
                        JOIN data_catalog dc_time ON sr.time_column_catalog_id = dc_time.id
                        LEFT JOIN data_catalog dc_cat ON sr.category_column_catalog_id = dc_cat.id
                        WHERE sr.is_active = TRUE
                        AND (sr.status_column_catalog_id IN ({format_strings}) OR 
                             sr.time_column_catalog_id IN ({format_strings}) OR
                             sr.category_column_catalog_id IN ({format_strings}))
                    """, tuple(catalog_ids * 3))
                    
                    rules = cur.fetchall()
                    
                    if rules:
                        # Deduplicate by id
                        seen_rule_ids = set()
                        lines.append("\n## Status Rules (Downtime Analysis)")
                        for rule in rules:
                            if rule["id"] in seen_rule_ids:
                                continue
                            seen_rule_ids.add(rule["id"])
                            
                            rule_line = (
                                f"- status_rule_id={rule['id']}; "
                                f"rule_name={rule['name']}; "
                                f"data_source_id={rule['data_source_id']}; "
                                f"schema={rule['schema_name']}; "
                                f"table={rule['table_name']}; "
                                f"time_column={rule['time_column']}; "
                                f"status_column={rule['status_column']}; "
                            )
                            if rule['category_column']:
                                rule_line += f"category_column={rule['category_column']}; "
                            rule_line += f"description={rule['description']}"
                            
                            lines.append(rule_line)
        except Exception as e:
            # Silently fail if DB is not available for rules lookup
            pass

    return "\n".join(lines)
