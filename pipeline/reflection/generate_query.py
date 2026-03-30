from model.gpt import get_llm_response_sys

def generation_query(information_verified, information_table):
    system_prompt = """
    You are an expert SQL generator for data verification.

    You are given:
    1. A database schema (tables and columns)
    2. A list of VERIFIED claims (each claim already includes table and columns)

    Your task:
    Generate ONE SQL query for EACH claim to verify it.

    STRICT RULES:
    - You MUST use the EXACT table and columns provided in each claim
    - DO NOT use any column outside the "columns" field of the claim
    - DO NOT invent tables or columns
    - Each SQL must be executable

    LOGIC RULES:
    - Numerical claims → return exact values for entities mentioned
    - Comparison claims → return both values in the SAME query for comparison
    - Trend claims → return values across time columns (e.g., 2011 vs 2014)

    SQL RULES:
    - Only use SELECT
    - Use WHERE to filter entities (e.g., Country = 'Vietnam')
    - Use IN when multiple entities appear
    - Wrap table names with spaces using backticks: `table name`
    - Wrap column names with spaces using brackets: [column name]

    OUTPUT FORMAT (JSON list):
    [
    {
        "claim": "...",
        "sql": "...",
        "explanation": "short explanation"
    }
    ]

    Only return JSON. No markdown. No text outside JSON.
    """
    user_prompt = f"""
    Database schema:
    {information_table}

    Claims:
    {information_verified}

    Generate SQL queries to verify each claim.
    """
    return get_llm_response_sys(system_prompt, user_prompt)