from fastapi import APIRouter, HTTPException
from app.models.data_source import DataSourceCreate, DataSourceResponse
from app.services.data_source_service import create_data_source, test_connection
from app.services.schema_scanner import scan_data_source

router = APIRouter()

@router.post("")
def add_data_source(ds: DataSourceCreate):
    try:
        ds_id = create_data_source(ds)
        return {"message": "Data source created", "id": ds_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{ds_id}/test")
def test_data_source(ds_id: int):
    try:
        success = test_connection(ds_id)
        return {"message": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{ds_id}/scan")
def scan_source(ds_id: int):
    try:
        count = scan_data_source(ds_id)
        return {"message": f"Scanned {count} columns successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
