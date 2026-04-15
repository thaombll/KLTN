from model import gpt
from model.gpt import get_llm_response_sys
from model.clean_json import parse_llm_output
from model.clean_json import llm_output_to_df

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

from pipeline.narration.map_plot import map_plot
from pipeline.narration.template_code_plot import plot
from pipeline.narration.explanable_plot import explanable_plot

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
    # print(res)

    data = build_table_json(res)
    print(data)
    # information_table = understanding_table(data)
    # reflection_obj = Reflection(data)
    # reflection = reflection_obj.reflection()
    # information_verified = extract_information(information_table, reflection)
    # output = generation_query(information_verified, information_table)
    # print(output)

    # output = output.strip()
    # output = output.replace("```json", "").replace("```", "")
    # data = json.loads(output)

    # list_claim = []
    # list_query = []

    # for item in data:
    #     list_claim.append(item["claim"])
    #     list_query.append(item["sql"])

    # list_output_query = run_query(res, list_query)

    # list_feedback = []
    # list_suggest_fix = []
    # reflection_revision = reflection

    # for i in range (len(list_query)):
    #     verified = verified_information(information_table, list_claim[i], list_output_query[i])
    #     verified = verified.strip()
    #     verified = verified.replace("```json", "").replace("```", "")
    #     data = json.loads(verified)
    #     list_feedback.append(data["feedback"])
    #     list_suggest_fix.append(data["suggested_fix"])
    #     reflection_revision = revision_reflection(reflection_revision, list_claim[i], data["feedback"], data["suggested_fix"])

    # for i in range(len(list_claim)):
    #     print("------------------------------------------------------------------------")
    #     print(f'Claim: {list_claim[i]}')
    #     print(f'Query: {list_query[i]}')
    #     print(f'Feedback: {list_feedback[i]}')
    #     print(f'Suggest: {list_suggest_fix[i]}')

    # print("------------------------------------------------------------------------")
    # print(reflection_revision)

    # list_sentence = extract_reflection(reflection_revision)
    # print("------------------------------------------------------------------------")
    # print ("Result to node")

    # list_node = []
    # for i in range(len(list_sentence)):
    #     a = information_into_node(list_sentence[i])
    #     print(a)
    #     print(list_sentence[i])
    #     list_node.append(a)

    # # print("------------------------------------------------------------------------")
    # # print("Relationship node: ")

    # list_relationship = []
    # for i in range(len(list_node)):
    #     for j in range(i + 1, len(list_node)):
    #         relationship = build_relationship(list_node[i], list_node[j])
    #         print(relationship)
    #         if relationship != []:
    #             list_relationship.append(relationship)

    # order_sentence = define_outline(list_relationship, list_sentence)

    # print(outline_revision(order_sentence))
    outline = """[
        {
            "section_title": "Profitability Overview",
            "sentences": [
                "A wide range of profitability is exhibited across countries, with some experiencing significant losses, such as Argentina (18,694) and Turkey (98,447).",
                "By contrast, several countries demonstrate positive totals, notable examples being Algeria (9,107) and Angola (6,495)."
            ]
        },
        {
            "section_title": "Influence of Discount Strategies",
            "sentences": [
                "The data strongly suggests a relationship between discount rates and profit margins.",
                "Notable correlation between high discount rates and negative profits, primarily in countries like Nigeria and Zimbabwe, both experiencing the highest discount level, represented numerically as '1'.",
                "Countries with positive profits show no evidence of discounts, suggesting a direct impact of discounts on profitability.",
                "Countries with high discounts face greater sustained losses, indicating a likely causal relationship."
            ]
        },
        {
            "section_title": "Geographical and Market-Specific Nuances",
            "sentences": [
                "The variation suggests geographic or marketspecific nuances influencing the profitability, with nearly half of the countries facing negative profits.",
                "Different countries exhibit varying responses to discount strategies, suggesting market-specific analyses are necessary.",
                "Some countries maintain profitability without discounts, perhaps indicative of different market dynamics or consumer behavior."
            ]
        },
        {
            "section_title": "Implications of Declining Trends",
            "sentences": [
                "Persistent yearoveryear declines in profitability for many countries, such as Nigeria and Turkey, indicate a systemic issue.",
                "The trend of increasing losses over time aligns with ongoing and perhaps more aggressive discount offers, exacerbating profitability issues.",
                "Data indicates that negative profit countries do not experience faster growth than those with positive profits, challenging any assumptions that discounts spur growth.",
                "Percentage growth rates in both categories fluctuate considerably, with no apparent advantage in high discount regions."
            ]
        },
        {
            "section_title": "Strategic Recommendations",
            "sentences": [
                "These insights highlight a need to evaluate discount strategies as they appear detrimental in many regions.",
                "While some countries manage to remain profitable without such discounts, others are trapped in burgeoning losses, signaling a need for tailored strategies.",
                "Strategic overhaul in discount offerings may help reverse negative trends observed consistently over the years.",
                "The data narrates a cautionary tale of the adverse impacts of aggressive discount strategies on profit margins."
            ]
        },
        {
            "section_title": "Critical Regions Needing Attention",
            "sentences": [
                "Argentina and Turkey stand out with the highest negative profits, indicating urgent attention required in these regions."
            ]
        }
    ]"""
    print(map_plot(outline, data))
    list_plot = map_plot(outline, data)

    data = parse_llm_output(list_plot)
    df = llm_output_to_df(data)

    df = plot(df)

    explain_plot = []
    for i in range(len(df)):
        path_plot = df.iloc[i]["plot_path"]
        if isinstance(path_plot, str): 
            explain_plot.append(explanable_plot(path_plot))
        else:
            explain_plot.append("")

    df["explanable_plot"] = explain_plot

    print(df.head())