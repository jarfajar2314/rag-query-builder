from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.data_sources import router as data_sources_router

app = FastAPI(
    title="RAG Query Builder API",
    version="0.1.0"
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(catalog_router, prefix="/api/catalog", tags=["catalog"])
app.include_router(data_sources_router, prefix="/api/data-sources", tags=["data-sources"])