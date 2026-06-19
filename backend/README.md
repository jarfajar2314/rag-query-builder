# RAG Query Builder - Backend

This is the FastAPI backend application for the RAG Query Builder. It serves as the orchestrator between the database schema, OpenAI LLM, and the executed SQL queries.

## Features

- **Catalog Sync**: Reads schema metadata from PostgreSQL and maintains an active catalog in `data_catalog`.
- **Query Planner**: Extracts intents via OpenAI structured output to build a `QueryPlan` JSON object.
- **Date Parsing**: Normalizes natural language dates (e.g. "this month") into absolute timestamps.
- **SQL Templates**: Securely translates JSON plans into raw SQL (trend, summary, compare, raw_table).
- **Validation**: Enforces strict validation on tables, columns, and SQL commands (read-only enforcement).

## Stack

- FastAPI
- PostgreSQL (`psycopg`)
- Pydantic
- OpenAI API

## Development

First, set up your environment variables in `.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
OPENAI_API_KEY=your-openai-api-key
USE_OPENAI_INTENT=true
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run database migrations:
```bash
python scripts/run_migrations.py
```

Start the API server:
```bash
uvicorn app.main:app --reload
# Server will start on http://localhost:8000
```
