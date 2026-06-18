from typing import Any
from app.db.postgres import execute_select_query

def search_catalog(prompt: str) -> list[dict[str, Any]]:
    """
    Search data_catalog using simple keyword matching by splitting the prompt into words.
    """
    # Exclude common stop words
    stop_words = {"show", "me", "the", "this", "that", "in", "by", "per", "for", "a", "an", "is", "of", "and"}
    words = [w for w in prompt.lower().split() if w not in stop_words and len(w) > 2]
    
    if not words:
        words = [""] # Fallback to match nothing basically or everything
        
    where_clauses = []
    params = {}
    
    for i, word in enumerate(words):
        param_name = f"kw_{i}"
        params[param_name] = f"%{word}%"
        
        clause = f"""(
            dc.table_name ILIKE %({param_name})s
         OR dc.column_name ILIKE %({param_name})s
         OR dc.business_name ILIKE %({param_name})s
         OR dc.description ILIKE %({param_name})s
         OR dc.aliases ILIKE %({param_name})s
        )"""
        where_clauses.append(clause)
        
    or_condition = " OR ".join(where_clauses)

    sql = f"""
        WITH matched_tables AS (
            SELECT DISTINCT dc.data_source_id, dc.schema_name, dc.table_name
            FROM data_catalog dc
            WHERE dc.is_active = TRUE
              AND dc.is_queryable = TRUE
              AND ({or_condition})
        )
        SELECT
            dc.id,
            dc.data_source_id,
            ds.database_type,
            dc.schema_name,
            dc.table_name,
            dc.column_name,
            dc.column_type,
            dc.business_name,
            dc.description,
            dc.aliases,
            dc.unit,
            dc.is_time_column,
            dc.is_value_column,
            dc.is_category_column,
            dc.default_aggregation,
            dc.default_chart
        FROM data_catalog dc
        JOIN data_sources ds ON ds.id = dc.data_source_id
        JOIN matched_tables mt 
            ON mt.data_source_id = dc.data_source_id 
           AND mt.schema_name = dc.schema_name 
           AND mt.table_name = dc.table_name
        WHERE dc.is_active = TRUE
          AND dc.is_queryable = TRUE
        ORDER BY
            dc.table_name,
            dc.column_name
        LIMIT 200
    """

    return execute_select_query(sql, params)
