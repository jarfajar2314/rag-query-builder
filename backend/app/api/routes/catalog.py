from fastapi import APIRouter
from app.services.metadata_search import search_catalog

router = APIRouter()

@router.get("")
def get_catalog():
    items = search_catalog()
    return {"items": items}

@router.get("/tables")
def get_tables():
    items = search_catalog()
    tables = list(set(item["table_name"] for item in items))
    return {"tables": tables}

@router.get("/columns")
def get_columns():
    items = search_catalog()
    columns = list(set(item["column_name"] for item in items))
    return {"columns": columns}

from app.models.catalog import CatalogPatch
from app.services.catalog_service import patch_catalog_entry

@router.patch("/{catalog_id}")
def update_catalog(catalog_id: int, patch: CatalogPatch):
    try:
        updated = patch_catalog_entry(catalog_id, patch)
        return {"message": "Catalog updated", "entry": updated}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))
