from typing import Any
from pydantic import BaseModel
from app.db.postgres import execute_select_query
from app.models.user_request import UserRequestUnderstanding

class CatalogContextData(BaseModel):
    catalog_rows: list[dict[str, Any]]
    status_rules: list[dict[str, Any]]

def retrieve_metadata(understanding: UserRequestUnderstanding) -> CatalogContextData:
    words = []
    
    # Core mappings based on intent
    if understanding.intent == "downtime":
        words.extend(["stop", "downtime", "running", "status", "machine"])
    else:
        words.extend(understanding.metric_terms)
        words.extend(understanding.subject_terms)
        
    if not words:
        words = [""]
        
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
        
    or_condition = " OR ".join(where_clauses) if where_clauses else "1=1"
    
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
    
    catalog_rows = execute_select_query(sql, params)
    
    status_rules = []
    if catalog_rows:
        catalog_ids = [row["id"] for row in catalog_rows if "id" in row]
        if catalog_ids:
            format_strings = ','.join(['%(id)s'] * len(catalog_ids))
            # Just bind the same catalog_ids three times using a trick or explicit params
            params = {}
            for i, cid in enumerate(catalog_ids):
                params[f"cid_{i}"] = cid
                
            placeholders = ", ".join([f"%(cid_{i})s" for i in range(len(catalog_ids))])
            
            sr_sql = f"""
                SELECT 
                    sr.id as status_rule_id, sr.name as rule_name, sr.description, 
                    dc_stat.data_source_id, dc_stat.schema_name, dc_stat.table_name,
                    dc_time.column_name as time_column,
                    dc_stat.column_name as status_column,
                    dc_cat.column_name as category_column
                FROM status_rules sr
                JOIN data_catalog dc_stat ON sr.status_column_catalog_id = dc_stat.id
                JOIN data_catalog dc_time ON sr.time_column_catalog_id = dc_time.id
                LEFT JOIN data_catalog dc_cat ON sr.category_column_catalog_id = dc_cat.id
                WHERE sr.is_active = TRUE
                AND (sr.status_column_catalog_id IN ({placeholders}) OR 
                     sr.time_column_catalog_id IN ({placeholders}) OR
                     sr.category_column_catalog_id IN ({placeholders}))
            """
            # To pass parameters for three IN clauses, we just merge them in dict
            full_params = {}
            for i, cid in enumerate(catalog_ids):
                full_params[f"cid_{i}"] = cid
                
            raw_rules = execute_select_query(sr_sql, full_params)
            
            # deduplicate
            seen = set()
            for r in raw_rules:
                if r["status_rule_id"] not in seen:
                    seen.add(r["status_rule_id"])
                    status_rules.append(r)
            
    return CatalogContextData(
        catalog_rows=catalog_rows,
        status_rules=status_rules
    )
