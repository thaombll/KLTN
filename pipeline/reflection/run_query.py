from baseline.load_data import json2pd
import pandas as pd
import duckdb

def run_query(res, query):
    list_table_name = []
    list_table = []
    for item in res:
        for key in item:
            if key.startswith("paragraph"):
                idx = key.split("_")[-1]

                description = item[f"paragraph_{idx}"]
                title = item[f"table_{idx}_title"]
                table_file = item[f"table_{idx}"]
                table_file = table_file.replace('"', '')
                table_name = table_file.replace(".csv", '')
                list_table_name.append(table_name)
                list_table.append(pd.read_csv("data/Test/Tableau/tab_003/" + f"{table_file}"))
    
    con = duckdb.connect()

    for i in range(len(list_table_name)):
        con.register(list_table_name[i], list_table[i])

    result = con.execute(query).df()
    return result
    
if __name__ == "__main__":
    file_path = "data\\Test\\Tableau\\tableau_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['1']
    res = test_df.iloc[0]["paragraph_table_pair"]['1']
    query = f'''SELECT "Country", "Unnamed: 1" FROM "1Profit by country" WHERE [Country] IN ('Algeria', 'Angola');'''
    print(run_query(res, query))