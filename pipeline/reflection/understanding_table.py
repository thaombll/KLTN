from model.gpt import get_llm_response_sys
# from baseline.load_data import json2pd
# from pipeline.reflection.read_table import build_table_json

def understanding_table(tables):
    system_prompt = """
    You are an expert data analyst.

    You are given:
    - A table (dataframe-like structure)
    - A title and/or description of the table

    Your task is to understand the schema and semantics of the table.

    For each table, you must:

    1. Identify the table name (use the given title if available)

    2. List all columns exactly as they appear

    3. Infer the most appropriate data type for each column:
    - integer
    - float
    - string
    - categorical
    - date/time

    4. Explain the meaning of each column clearly based ONLY on:
    - the column name
    - the provided title/description
    - the values in the table

    5. Handle special cases:
    - Columns like "Unnamed: 0" likely represent row labels (e.g., metric names)
    - Columns that look like years (e.g., 2004, 2005, ...) represent time dimensions
    - Values like "5,763" should be interpreted as numeric (5763)
    - Missing values (NaN) should be treated as missing data

    6. If the table is in wide format (e.g., years as columns):
    - Recognize the implicit structure: (metric, time, value)
    - Explain this structure in the column descriptions

    IMPORTANT RULES:
    - Do NOT hallucinate meaning that is not supported by the data
    - If unsure about a column, say "unknown"
    - Be concise but precise
    - Use business-friendly language

    Return the result in STRICT JSON format:

    {
    "table_name": "...",
    "columns": [
        {
        "name": "...",
        "data_type": "...",
        "description": "..."
        }
    ]}
    """

    user_prompt = f"""
    TABLE :
    {tables}
    """
    return get_llm_response_sys(system_prompt, user_prompt)

# if __name__ == "__main__":
#     file_path = "data\\Test\\Tableau\\tableau_test.json"
#     test_df = json2pd(file_path)
#     intention = test_df.iloc[0]["intent"]['0']
#     res = test_df.iloc[0]["paragraph_table_pair"]['1']
#     data = build_table_json(res)
#     print(understanding_table(data))