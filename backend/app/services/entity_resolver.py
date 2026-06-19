from app.models.query_plan import QueryPlan
from app.db.postgres import execute_select_query

def resolve_entities(plan: QueryPlan) -> QueryPlan:
    """
    Verifies that category values extracted by the AI actually exist in the database.
    Prevents hallucinated filters like WHERE machine_name = 'NonExistent Machine'.
    """
    if plan.status != "ready" or not plan.category_column or not plan.category_value:
        return plan
        
    # Strip any accidental surrounding quotes from the AI's extraction
    clean_val = str(plan.category_value).strip("'\"")
    
    # Security: Ensure column/schema/table are simple identifiers, not injected SQL
    # We rely on the fact that these came from our validated data_catalog rows
    # but ILIKE provides safety against user-input category values.
    
    sql = f"""
        SELECT DISTINCT {plan.category_column}
        FROM {plan.schema_name}.{plan.table_name}
        WHERE {plan.category_column}::text ILIKE %(search_value)s
        ORDER BY {plan.category_column}
        LIMIT 20;
    """
    
    params = {
        "search_value": f"%{clean_val}%"
    }
    
    rows = execute_select_query(sql, params)
    
    if not rows:
        plan.status = "unsupported"
        plan.explanation = f"Entity '{clean_val}' not found in {plan.table_name}.{plan.category_column}."
        return plan
        
    if len(rows) == 1:
        # Exact/Single match - update the plan to match exact database casing/value
        plan.category_value = str(rows[0][plan.category_column])
        return plan
        
    # Several possible matches
    options = [str(r[plan.category_column]) for r in rows]
    plan.status = "needs_clarification"
    if "category_value" not in plan.missing_fields:
        plan.missing_fields.append("category_value")
        
    plan.clarification_question = f"I found multiple matches for '{plan.category_value}'. Which one did you mean? ({', '.join(options)})"
    
    return plan
