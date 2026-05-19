from baseline.load_data import json2pd
import pandas as pd
import duckdb
import chardet

def run_query(file_path, tables, list_query):
    list_table_name = []
    list_table = []
    list_output_query = []
    
    blocks = tables.strip().split("Table_name:")
    for block in blocks:
        if not block.strip():  
            continue
        lines = block.strip().split("\n")
        table_name = lines[0].strip()
        list_table_name.append(table_name)

    for i in range(len(list_table_name)):
        table_path = f"{file_path}/{list_table_name[i]}.csv"
        try:
            with open(table_path, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']
            df = pd.read_csv(table_path, encoding=encoding, sep=None, engine='python')
            df.columns = df.columns.str.strip()  # strip tên cột
            list_table.append(df)
        except FileNotFoundError:
            print(f"File not found: {table_path}")
            list_table.append(pd.DataFrame())
    
    con = duckdb.connect()

    for i in range(len(list_table_name)):
        if not list_table[i].empty:
            con.register(list_table_name[i], list_table[i])

    for i in range(len(list_query)):
        try:
            result = con.execute(list_query[i]).df()
            list_output_query.append(result)
        except Exception as e:
            print(f"Query error: {list_query[i]} -> {e}")
            list_output_query.append(None)
        
    return list_output_query