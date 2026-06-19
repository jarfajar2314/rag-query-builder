from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any

from app.config import settings
from app.services.request_understanding import understand_user_request
from app.services.metadata_retriever import retrieve_metadata
from app.services.grounded_plan_builder import build_grounded_query_plan
from app.services.entity_resolver import resolve_entities
from app.services.query_plan_validator import validate_plan_against_catalog
from app.services.sql_generator import generate_sql
from app.services.sql_validator import validate_sql
from app.services.query_executor import execute_plan_sql
from app.services.chart_builder import build_chart_config
from app.services.date_parser import parse_date_range

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("")
def chat(request: ChatRequest):
    try:
        # Step 1: Understand user intent natively
        understanding = understand_user_request(request.prompt)

        # Step 2: Retrieve metadata based on parsed concepts
        catalog_context = retrieve_metadata(understanding=understanding)
        
        if not catalog_context.catalog_rows:
            raise HTTPException(
                status_code=404,
                detail="No matching catalog metadata found for the extracted concepts."
            )

        # Step 3: Ground the understanding into a database query plan
        plan = build_grounded_query_plan(
            prompt=request.prompt,
            understanding=understanding,
            catalog_context=catalog_context
        )

        # Step 4: Handle Clarifications or Unsupported queries
        if plan.status == "needs_clarification":
            return {
                "status": plan.status,
                "question": plan.clarification_question,
                "missing_fields": plan.missing_fields,
            }
            
        if plan.status == "unsupported":
            raise HTTPException(
                status_code=400,
                detail=plan.explanation or "This query is unsupported by the current database metadata."
            )

        # Step 5: Resolve entities against the database
        resolved_plan = resolve_entities(plan)
        if resolved_plan.status == "needs_clarification":
            return {
                "status": resolved_plan.status,
                "question": resolved_plan.clarification_question,
                "missing_fields": resolved_plan.missing_fields,
            }
        if resolved_plan.status == "unsupported":
             raise HTTPException(
                status_code=400,
                detail=resolved_plan.explanation or "Entity resolution failed."
            )

        # Step 6: Normalize Plan Dates
        # If the plan is missing start_time or end_time, use the fallback date parser
        if not resolved_plan.start_time or not resolved_plan.end_time:
            parsed_dates = parse_date_range(request.prompt)
            if parsed_dates:
                resolved_plan.start_time = parsed_dates["start_time"]
                resolved_plan.end_time = parsed_dates["end_time"]
                
        # Fill in time column if missing but needed
        if not resolved_plan.time_column:
            for row in catalog_context.catalog_rows:
                if row.get("is_time_column"):
                    resolved_plan.time_column = row["column_name"]
                    break

        # Step 7: Validate against schema definitions
        validate_plan_against_catalog(
            plan=resolved_plan,
            catalog_rows=catalog_context.catalog_rows
        )

        # Step 8: Generate and execute SQL securely
        sql, params = generate_sql(resolved_plan)
        validate_sql(sql)
        
        rows = execute_plan_sql(sql, params, resolved_plan.model_dump())
        chart = build_chart_config(resolved_plan, rows)

        return {
            "answer": "Query executed successfully.",
            "prompt": request.prompt,
            "status": "success",
            "planner_source": "nlu_grounded",
            "understanding": understanding.model_dump(),
            "plan": resolved_plan.model_dump(),
            "sql": sql,
            "params": params,
            "rows": rows,
            "chart": chart,
            "catalog_matches": catalog_context.catalog_rows,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
