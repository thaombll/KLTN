from model import gpt
from model.gpt import get_llm_response_sys

def extract_information(information_table, reflection):
    system_prompt = """
    You are a data verification assistant.

    You are given:
    1. A reflection text containing insights.
    2. A database schema describing available tables and columns.

    Your task:
    Extract ONLY claims that can be VERIFIED using SQL queries based on the GIVEN schema.

    STRICT RULES:
    - A claim is valid ONLY IF it can be mapped to EXISTING tables and columns.
    - You MUST identify which table and columns are required to verify the claim.
    - If a claim cannot be expressed using the schema → DISCARD it.

    Keep ONLY claims that:
    - Contain explicit numerical values (e.g., 5.7, 3.0, 1.4)
    - OR contain clear comparisons (higher, lower, greater than, less than)
    - OR describe trends across clearly defined time periods (e.g., 2011 vs 2014, Q1 vs Q2)

    The claim MUST:
    - Be directly translatable into a SQL query (SELECT, GROUP BY, WHERE, etc.)
    - Use ONLY columns that exist in the schema

    Do NOT extract:
    - Abstract conclusions (e.g., "there is a relationship")
    - Causal explanations (e.g., "because", "due to")
    - Vague trends without numbers or clear groups
    - Any claim that requires external knowledge

    Output format (JSON list):
    Each item must contain:
    - "claim": exact sentence from the reflection
    - "type": "numerical" | "comparison" | "trend"
    - "table": table name used
    - "columns": list of columns used
    - "reason": short explanation why it is SQL-verifiable

    Only return JSON.
    """

    user_prompt = f"""
    Database schema:
    {information_table}

    Reflection:
    \"\"\"
    {reflection}
    \"\"\"

    Extract ONLY verifiable claims that can be answered using SQL on this schema.
    """

    return get_llm_response_sys(system_prompt, user_prompt)
