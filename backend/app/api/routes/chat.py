from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.services.metadata_search import search_catalog
from app.services.catalog_context_builder import build_catalog_context
from app.services.intent_extractor import extract_query_plan_with_openai
from app.services.query_planner import build_query_plan_from_catalog
from app.services.query_plan_validator import validate_plan_against_catalog
from app.services.sql_generator import generate_sql
from app.services.sql_validator import validate_sql
from app.services.query_executor import execute_plan_sql
from app.services.chart_builder import build_chart_config

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("")
def chat(request: ChatRequest):
    try:
        catalog_rows = search_catalog(request.prompt)

        if not catalog_rows:
            raise HTTPException(
                status_code=404,
                detail="No matching catalog metadata found."
            )

        planner_source = "rule_based"

        if settings.use_openai_intent and settings.openai_api_key:
            try:
                catalog_context = build_catalog_context(catalog_rows)

                plan_obj = extract_query_plan_with_openai(
                    prompt=request.prompt,
                    catalog_context=catalog_context
                )

                validate_plan_against_catalog(
                    plan=plan_obj,
                    catalog_rows=catalog_rows
                )

                planner_source = "openai"

            except Exception as e:
                print("OpenAI Planning failed, falling back to rule-based:", str(e))
                plan_obj = build_query_plan_from_catalog(
                    prompt=request.prompt,
                    catalog_rows=catalog_rows
                )

                validate_plan_against_catalog(
                    plan=plan_obj,
                    catalog_rows=catalog_rows
                )

                planner_source = "rule_based_fallback"
        else:
            plan_obj = build_query_plan_from_catalog(
                prompt=request.prompt,
                catalog_rows=catalog_rows
            )

            validate_plan_against_catalog(
                plan=plan_obj,
                catalog_rows=catalog_rows
            )

        plan = plan_obj.model_dump()

        sql = generate_sql(plan)
        
        params = {}
        if "start_time" in plan and "end_time" in plan:
            params = {
                "start_time": plan["start_time"],
                "end_time": plan["end_time"]
            }

        validate_sql(sql)

        rows = execute_plan_sql(sql, params, plan)

        chart = build_chart_config(plan, rows)

        return {
            "answer": "Query executed successfully.",
            "prompt": request.prompt,
            "planner_source": planner_source,
            "plan": plan,
            "sql": sql,
            "params": params,
            "rows": rows,
            "chart": chart,
            "catalog_matches": catalog_rows,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )