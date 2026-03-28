import json
import pandas as pd

def json2pd(file_path):
    with open(file_path) as f:
        temp_data = [json.loads(line) for line in f]
    df = pd.DataFrame(temp_data)
    return df