from model.gpt import get_llm_response_sys
from baseline.load_data import json2pd
from pipeline.reflection.read_table import build_table_json

def understanding_table(intention, information_table):

    system_prompt = """
    You are an expert data analyst.
    You are given:
    - An intention (the story/topic the data is meant to tell)
    - Multiple tables, each in the following text format:
        Table_name: <name>
        Data:
        <table content>

    IMPORTANT:
    - The value after "Table_name:" is the ONLY valid table name
    - You MUST copy it EXACTLY to the output
    - DO NOT modify, summarize, or infer a new name

    Your task is to understand the schema and semantics of the table IN THE CONTEXT of the given intention.

    Instructions:

    1. Table name:
    - Extract value after "Table_name:" 
    - Copy it EXACTLY into output

    2. List all columns exactly as they appear in the Data section

    3. Infer the most appropriate data type for each column:
    - integer
    - float
    - string
    - categorical
    - date/time

    4. Explain the meaning of each column based on:
    - column name
    - intention
    - values in table

    5. Handle special cases:
    - "Unnamed: 0" → likely row labels
    - Year columns → time dimension
    - "5,763" → numeric (5763)
    - NaN → missing data

    6. If wide format:
    - Recognize (metric, time, value)

    RULES:
    - DO NOT hallucinate
    - If unsure → "unknown"
    - Be concise and precise

    Output STRICT JSON:
    {
        "table_name": "<EXACT VALUE AFTER Table_name:>",
        "columns": [
            {
                "name": "...",
                "data_type": "...",
                "description": "..."
            }
        ]
    }
    """

    user_prompt = f"""
    INTENTION: {intention}

    TABLE:
    {information_table}
    """

    return get_llm_response_sys(system_prompt, user_prompt)