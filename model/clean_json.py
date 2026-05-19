import json
import re
import pandas as pd

def clean_llm_json(output_str):
    output_str = re.sub(r"```json|```", "", output_str).strip()
    match = re.search(r"\[.*\]", output_str, re.DOTALL)
    if match:
        output_str = match.group(0)

    return output_str


def parse_llm_output(output_str):
    clean_str = clean_llm_json(output_str)
    
    try:
        return json.loads(clean_str)
    except json.JSONDecodeError:
        print("JSON lỗi, thử fix nhẹ...")
    
    try:
        # Fix trailing comma
        clean_str = re.sub(r",\s*}", "}", clean_str)
        clean_str = re.sub(r",\s*]", "]", clean_str)
        return json.loads(clean_str)
    except json.JSONDecodeError:
        print("JSON lỗi, thử fix mạnh hơn...")
    
    try:
        # Fix single quotes
        clean_str = clean_str.replace("'", '"')
        return json.loads(clean_str)
    except json.JSONDecodeError:
        pass

    try:
        # Dùng ast
        import ast
        return ast.literal_eval(clean_str)
    except:
        pass

    # In ra để debug
    lines = clean_str.split('\n')
    print(f"Lỗi gần line 78:\n{''.join(lines[75:80])}")
    raise ValueError(f"Cannot parse JSON:\n{clean_str[:500]}")

def llm_output_to_df(data):
    rows = []

    for item in data:
        row = {
            "section": item.get("section"),
            "plot_type": item.get("plot_type"),
            "table_name": item.get("table_name"),
            "no_plot": item.get("no_plot"),
            "reason": item.get("reason"),

            "x": item.get("plot_params", {}).get("x"),
            "y": item.get("plot_params", {}).get("y"),
            "size": item.get("plot_params", {}).get("size"),
            "bar_values": item.get("plot_params", {}).get("bar_values"),
            "line_values": item.get("plot_params", {}).get("line_values"),

            "title": item.get("labels", {}).get("title"),
            "xlabel": item.get("labels", {}).get("xlabel"),
            "ylabel": item.get("labels", {}).get("ylabel"),
            "ylabel_bar": item.get("labels", {}).get("ylabel_bar"),
            "ylabel_line": item.get("labels", {}).get("ylabel_line"),
        }

        rows.append(row)

    return pd.DataFrame(rows)