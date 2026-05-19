import os
import pandas as pd
from baseline.load_data import json2pd

def build_table_json(res, base_path="data/Test/Tableau/tab_003"):
    output = []

    for item in res:
        for key in item:
            if key.startswith("paragraph"):
                idx = key.split("_")[-1]

                description = item[f"paragraph_{idx}"]
                title = item[f"table_{idx}_title"]
                table_file = item[f"table_{idx}"]
                table_file = table_file.replace('"', '')
                table_name = table_file.replace(".csv", '')
                # print("---------------------")
                # print(table_name)

                table_path = os.path.join(base_path, table_file)
                df = pd.read_csv(table_path)

                output.append({
                    "description": description,
                    "title": title,
                    "table name": table_name,
                    "table": df
                })
    return output

if __name__ == "__main__":
    file_path = "data\\Test\\Tableau\\tableau_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['1']
    res = test_df.iloc[0]["paragraph_table_pair"]['1']
    print(build_table_json(res, "data\\Test\\Tableau\\tab_003"))
