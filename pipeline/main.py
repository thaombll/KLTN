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

from pipeline.outline.extract_information import extract_reflection
from pipeline.outline.information_into_node import information_into_node
from pipeline.outline.relationship_node import build_relationship
from pipeline.outline.define_outline import define_outline
from pipeline.outline.outline import outline_revision
import json

if __name__ == "__main__":
    # file_path = "data\\Test\\Pew\\pew_test.json"
    # test_df = json2pd(file_path)
    # intention = test_df.iloc[0]["intent"]['0']
    # res = test_df.iloc[0]["paragraph_table_pair"]['1']
    # tables = ''
    # for x, item in enumerate(res):
    #     tables += f'### Table_{x}:\n{item["paragraph"]}\n'

    # print(tables)

    # print(f'Res: {res}')

    file_path = "data\\Test\\Tableau\\tableau_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['1']
    res = test_df.iloc[0]["paragraph_table_pair"]['1']
    print(res)

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
    reflection_revision = reflection

    for i in range (len(list_query)):
        verified = verified_information(information_table, list_claim[i], list_output_query[i])
        verified = verified.strip()
        verified = verified.replace("```json", "").replace("```", "")
        data = json.loads(verified)
        list_feedback.append(data["feedback"])
        list_suggest_fix.append(data["suggested_fix"])
        reflection_revision = revision_reflection(reflection_revision, list_claim[i], data["feedback"], data["suggested_fix"])

    for i in range(len(list_claim)):
        print("------------------------------------------------------------------------")
        print(f'Claim: {list_claim[i]}')
        print(f'Query: {list_query[i]}')
        print(f'Feedback: {list_feedback[i]}')
        print(f'Suggest: {list_suggest_fix[i]}')

    print("------------------------------------------------------------------------")
    print(reflection_revision)

    list_sentence = extract_reflection(reflection_revision)
    print("------------------------------------------------------------------------")
    print ("Result to node")

    list_node = []
    for i in range(len(list_sentence)):
        a = information_into_node(list_sentence[i])
        print(a)
        print(list_sentence[i])
        list_node.append(a)

    # print("------------------------------------------------------------------------")
    # print("Relationship node: ")

    list_relationship = []
    for i in range(len(list_node)):
        for j in range(i + 1, len(list_node)):
            relationship = build_relationship(list_node[i], list_node[j])
            if relationship != []:
                list_relationship.append(relationship)
    order_sentence = define_outline(list_relationship, list_sentence)
    
    print(outline_revision(order_sentence))
    