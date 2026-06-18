from app.db.postgres import execute_select_query
from app.models.catalog import CatalogPatch

def patch_catalog_entry(catalog_id: int, patch: CatalogPatch):
    """
    Update a catalog entry with manual enrichment.
    Only updates fields that are provided.
    """
    fields = patch.model_dump(exclude_unset=True)
    if not fields:
        return get_catalog_entry(catalog_id)
        
    set_clauses = []
    params = {"id": catalog_id}
    
    for key, value in fields.items():
        set_clauses.append(f"{key} = %({key})s")
        params[key] = value
        
    set_string = ", ".join(set_clauses)
    
    sql = f"""
        UPDATE data_catalog
        SET {set_string}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %(id)s
        RETURNING *
    """
    
    rows = execute_select_query(sql, params)
    if not rows:
        raise ValueError(f"Catalog entry {catalog_id} not found")
        
    return rows[0]
    
def get_catalog_entry(catalog_id: int):
    sql = "SELECT * FROM data_catalog WHERE id = %(id)s"
    rows = execute_select_query(sql, {"id": catalog_id})
    return rows[0] if rows else None
