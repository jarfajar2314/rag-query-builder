from fastapi import APIRouter

from app.db.postgres import test_postgres_connection

router = APIRouter()


@router.get("")
def health_check():
    return {
        "status": "ok"
    }


@router.get("/db")
def database_health_check():
    is_connected = test_postgres_connection()

    return {
        "status": "ok" if is_connected else "error",
        "database": "postgresql",
        "connected": is_connected
    }