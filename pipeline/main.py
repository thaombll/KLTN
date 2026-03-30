from model import gpt
from model.gpt import get_llm_response_sys
from pipeline.reflection.understanding_table import understanding_table
from baseline.load_data import json2pd
from pipeline.reflection.read_table import build_table_json
from baseline.reflection import Reflection
from pipeline.reflection.extract_infomation_verified import extract_information
from pipeline.reflection.generate_query import generation_query

if __name__ == "__main__":
    file_path = "data\\Test\\Tableau\\tableau_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['0']
    res = test_df.iloc[0]["paragraph_table_pair"]['1']

    data = build_table_json(res)
    information_table = understanding_table(data)
    reflection_obj = Reflection(data)
    reflection = reflection_obj.reflection()
    information_verified = extract_information(information_table, reflection)
    print(generation_query(information_verified, information_table))
    