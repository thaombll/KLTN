from model import gpt
from model.gpt import get_llm_response_sys
from pipeline.reflection.understanding_table import understanding_table
from baseline.load_data import json2pd
from pipeline.reflection.read_table import build_table_json
from baseline.reflection import Reflection
from pipeline.reflection.extract_infomation_verified import extract_information
from pipeline.reflection.generate_query import generation_query
from pipeline.reflection.run_query import run_query
from pipeline.reflection.verified_information import verified_information
from pipeline.reflection.revision_reflection import revision_reflection
import json

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
    output = generation_query(information_verified, information_table)
    print(output)

    output = output.strip()
    output = output.replace("```json", "").replace("```", "")
    data = json.loads(output)

    list_claim = []
    list_query = []

    for item in data:
        list_claim.append(item["claim"])
        list_query.append(item["sql"])

    list_output_query = run_query(res, list_query)

    list_feedback = []
    list_suggest_fix = []
    reflection_fix = []

    for i in range (len(list_query)):
        verified = verified_information(information_table, list_claim[i], list_output_query[i])
        verified = verified.strip()
        verified = verified.replace("```json", "").replace("```", "")
        data = json.loads(verified)
        list_feedback.append(data["feedback"])
        list_suggest_fix.append(data["suggested_fix"])
        reflection_fix.append(revision_reflection(reflection, list_claim[i], data["feedback"], data["suggested_fix"]))
    print(reflection_fix)

    