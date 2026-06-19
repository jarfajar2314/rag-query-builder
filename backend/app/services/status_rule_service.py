import json
from typing import Any

from psycopg.rows import dict_row

from app.db.postgres import get_postgres_connection
from app.models.status_rule import StatusRuleCreate, StatusRuleUpdate

def create_status_rule(rule: StatusRuleCreate) -> dict[str, Any]:
    with get_postgres_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            # Validate cross-column relationships
            col_ids = [rule.status_column_catalog_id, rule.time_column_catalog_id]
            if rule.category_column_catalog_id is not None:
                col_ids.append(rule.category_column_catalog_id)

            format_strings = ','.join(['%s'] * len(col_ids))
            cursor.execute(
                f"""
                SELECT data_source_id, schema_name, table_name 
                FROM data_catalog 
                WHERE id IN ({format_strings})
                """,
                tuple(col_ids)
            )
            rows = cursor.fetchall()
            
            if len(rows) != len(col_ids):
                raise ValueError("One or more column catalog IDs do not exist.")
            
            # Check they all belong to same table
            first_row = rows[0]
            for row in rows[1:]:
                if (row['data_source_id'] != first_row['data_source_id'] or 
                    row['schema_name'] != first_row['schema_name'] or 
                    row['table_name'] != first_row['table_name']):
                    raise ValueError("All columns in a status rule must belong to the same data source, schema, and table.")

            # Insert rule
            cursor.execute(
                """
                INSERT INTO status_rules (
                    name, description, status_column_catalog_id, time_column_catalog_id, 
                    category_column_catalog_id, running_values, downtime_values, 
                    expected_interval_seconds, gap_tolerance_seconds, minimum_downtime_seconds
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING id
                """,
                (
                    rule.name,
                    rule.description,
                    rule.status_column_catalog_id,
                    rule.time_column_catalog_id,
                    rule.category_column_catalog_id,
                    json.dumps(rule.running_values),
                    json.dumps(rule.downtime_values),
                    rule.expected_interval_seconds,
                    rule.gap_tolerance_seconds,
                    rule.minimum_downtime_seconds
                )
            )
            new_id = cursor.fetchone()["id"]
            conn.commit()
            return get_status_rule(new_id)

def get_status_rules() -> list[dict[str, Any]]:
    with get_postgres_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM status_rules ORDER BY id")
            return cursor.fetchall()

def get_status_rule(rule_id: int) -> dict[str, Any]:
    with get_postgres_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM status_rules WHERE id = %s", (rule_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Status rule {rule_id} not found.")
            return row

def update_status_rule(rule_id: int, updates: StatusRuleUpdate) -> dict[str, Any]:
    # Basic implementation without deep validation for MVP brevity
    with get_postgres_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM status_rules WHERE id = %s", (rule_id,))
            if not cursor.fetchone():
                raise ValueError(f"Status rule {rule_id} not found.")
            
            update_data = updates.model_dump(exclude_unset=True)
            if not update_data:
                return get_status_rule(rule_id)
            
            # Serialize JSON
            if "running_values" in update_data:
                update_data["running_values"] = json.dumps(update_data["running_values"])
            if "downtime_values" in update_data:
                update_data["downtime_values"] = json.dumps(update_data["downtime_values"])

            set_clauses = [f"{k} = %s" for k in update_data.keys()]
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            
            query = f"UPDATE status_rules SET {', '.join(set_clauses)} WHERE id = %s"
            values = list(update_data.values()) + [rule_id]
            
            cursor.execute(query, tuple(values))
            conn.commit()
            return get_status_rule(rule_id)
