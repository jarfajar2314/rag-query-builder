from app.db.postgres import execute_select_query
from app.services.data_source_service import get_data_source
import psycopg
from psycopg.rows import dict_row

def scan_data_source(ds_id: int):
    ds = get_data_source(ds_id)
    
    if ds["database_type"] != "postgresql":
        raise ValueError("Only PostgreSQL scanning is supported right now")
        
    # Connect directly to the target DB
    conn = psycopg.connect(
        host=ds["host"],
        port=ds["port"],
        dbname=ds["database_name"],
        user=ds["username"],
        password=ds["password_encrypted"],
        row_factory=dict_row
    )
    
    # Run info schema query
    sql = """
        SELECT
            table_schema AS schema_name,
            table_name,
            column_name,
            data_type AS column_type
        FROM information_schema.columns
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name, ordinal_position;
    """
    
    with conn.cursor() as cur:
        cur.execute(sql)
        scanned_columns = cur.fetchall()
        
    conn.close()
    
    # Upsert logic into data_catalog
    upsert_sql = """
        INSERT INTO data_catalog 
        (data_source_id, schema_name, table_name, column_name, column_type)
        VALUES (%(ds_id)s, %(schema)s, %(table)s, %(col)s, %(type)s)
        ON CONFLICT (data_source_id, schema_name, table_name, column_name)
        DO UPDATE SET 
            column_type = EXCLUDED.column_type,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id;
    """
    
    for col in scanned_columns:
        params = {
            "ds_id": ds_id,
            "schema": col["schema_name"],
            "table": col["table_name"],
            "col": col["column_name"],
            "type": col["column_type"]
        }
        execute_select_query(upsert_sql, params)
        
    return len(scanned_columns)
