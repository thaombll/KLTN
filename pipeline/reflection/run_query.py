from baseline.load_data import json2pd
import pandas as pd
import duckdb

def run_query(res, list_query):
    list_table_name = []
    list_table = []
    list_output_query = []
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

    for i in range (len(list_query)):
        list_output_query.append(con.execute(list_query[i]).df())
        
    return list_output_query
    
# if __name__ == "__main__":
#     file_path = "data\\Test\\Tableau\\tableau_test.json"
#     test_df = json2pd(file_path)
#     intention = test_df.iloc[0]["intent"]['1']
#     res = test_df.iloc[0]["paragraph_table_pair"]['1']
#     query = f'''SELECT \"Unnamed: 0\", \"Order Date\", \"Order Date.3\" FROM \"4Profit over time\" WHERE \"Unnamed: 0\" = 'Turkey';'''
#     print(run_query(res, query))