from model.gpt import get_llm_response_sys
import os
import re
from baseline.load_data import json2pd

def reconstruct_table(tables):
    system_prompt = """
    You are an expert in data extraction, table reconstruction, and data understanding.

    The input is messy text extracted from reports or charts.

    Your tasks:
    1. Identify each table separately
    2. Reconstruct each table into a clean and readable table
    3. Detect correct columns and rows
    4. Fix broken numbers (e.g., "2. 6" -> 2.6)
    5. Preserve important titles and context (do NOT remove them)
    6. Remove only irrelevant noise (e.g., sources, notes if not useful)
    7. Ensure all rows have consistent number of columns
    8. Infer and standardize correct data types for each column

    Data type rules:
    - Integers: 1, 25, 100
    - Floats: 1.5, 2.75
    - Percentages: convert to float (e.g., "25%" -> 25.0)
    - Dates: use ISO format if possible
    - Categories: clean strings (no extra spaces)
    - Missing values: leave empty

    IMPORTANT:
    - Keep the original meaning and context of the table
    - Keep titles to make the table understandable
    - Output must be clean and human-readable (CSV-like format)
    - Do NOT output JSON
    - Do NOT include explanations

    Return format:

    TABLE: <table_name>
    TITLE: <table title or inferred title>
    DESCRIPTION: <what this table shows>

    col1,col2,col3,...
    value1,value2,value3,...

    Separate tables using a blank line.
    """

    user_prompt = f"""
    Reconstruct the following messy tables into clean, readable tables:

    {tables}
    """

    return get_llm_response_sys(system_prompt, user_prompt)

if __name__ == "__main__":
    file_path = "data\\Test\\Tableau\\tableau_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['0']
    res = test_df.iloc[0]["paragraph_table_pair"]['0']
    print(res)
    # tables = ''
  
    # for x, item in enumerate(res):
    #     tables += f'### Table_{x}:\n{item["table"]}\n'
    # print("-------------------------------------------------------------------------")
    # print(tables)
    # print("-------------------------------------------------------------------------")
    # print(reconstruct_table(tables))
    

# def save_tables_to_csv(llm_output, output_dir="model_generation"):
#     os.makedirs(output_dir, exist_ok=True)

#     tables = llm_output.strip().split("\n\n")

#     for table in tables:
#         lines = table.strip().split("\n")
        
#         if not lines or not lines[0].startswith("TABLE:"):
#             continue
        
#         # Lấy tên bảng
#         table_name = lines[0].replace("TABLE:", "").strip()
        
#         # Clean tên file (tránh lỗi ký tự)
#         table_name = re.sub(r'[^\w\-]', '_', table_name)

#         csv_content = "\n".join(lines[1:])
#         file_path = os.path.join(output_dir, f"{table_name}.csv")

#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(csv_content)

#         print(f"✅ Saved: {file_path}")