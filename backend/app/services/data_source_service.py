from app.db.postgres import execute_select_query
from app.models.data_source import DataSourceCreate
import psycopg

def create_data_source(ds: DataSourceCreate):
    sql = """
        INSERT INTO data_sources 
        (name, database_type, host, port, database_name, username, password_encrypted, default_schema)
        VALUES (%(name)s, %(type)s, %(host)s, %(port)s, %(db)s, %(user)s, %(pass)s, %(schema)s)
        RETURNING id
    """
    params = {
        "name": ds.name,
        "type": ds.database_type,
        "host": ds.host,
        "port": ds.port,
        "db": ds.database_name,
        "user": ds.username,
        "pass": ds.password, # Plain text for MVP
        "schema": ds.default_schema
    }
    
    rows = execute_select_query(sql, params)
    return rows[0]["id"]

def get_data_source(ds_id: int):
    sql = "SELECT * FROM data_sources WHERE id = %(id)s"
    rows = execute_select_query(sql, {"id": ds_id})
    if not rows:
        raise ValueError(f"Data source {ds_id} not found")
    return rows[0]

def test_connection(ds_id: int) -> bool:
    ds = get_data_source(ds_id)
    if ds["database_type"] == "postgresql":
        try:
            conn = psycopg.connect(
                host=ds["host"],
                port=ds["port"],
                dbname=ds["database_name"],
                user=ds["username"],
                password=ds["password_encrypted"]
            )
            conn.close()
            return True
        except Exception as e:
            raise ValueError(f"Connection failed: {str(e)}")
            
    raise ValueError(f"Unsupported testing for type {ds['database_type']}")
