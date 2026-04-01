from model.gpt import get_llm_response_sys
from baseline.load_data import json2pd
from pipeline.reflection.read_table import build_table_json

def understanding_table(information_table):

    system_prompt = """
    You are an expert data analyst.

    You are given a JSON object with the following structure:
    {
        "table_name": "...",
        "title": "...",
        "description": "...",
        "table": ...
    }

    IMPORTANT:
    - The field "table_name" inside the JSON is the ONLY valid table name
    - You MUST copy it EXACTLY to the output
    - DO NOT modify, summarize, or infer a new name
    - DO NOT use title as table name
    - If you change the table_name, the output is INVALID

    Your task is to understand the schema and semantics of the table.

    Instructions:

    1. Table name:
    - Extract "table_name" from the input JSON
    - Copy it EXACTLY into output

    2. List all columns exactly as they appear

    3. Infer the most appropriate data type for each column:
    - integer
    - float
    - string
    - categorical
    - date/time

    4. Explain the meaning of each column based ONLY on:
    - column name
    - title
    - description
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
        "table_name": "<EXACT VALUE FROM INPUT JSON.table_name>",
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
    INPUT JSON:
    {information_table}
    """

    return get_llm_response_sys(system_prompt, user_prompt)

if __name__ == "__main__":
    file_path = "data\\Test\\Tableau\\tableau_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['1']
    res = test_df.iloc[0]["paragraph_table_pair"]['1']
    data = build_table_json(res)
    print(understanding_table(data))