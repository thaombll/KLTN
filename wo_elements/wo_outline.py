from model import gpt
from model.gpt import get_llm_response_sys
from model.clean_json import parse_llm_output
from model.clean_json import llm_output_to_df
import time
from model.gpt import token_usage

from pipeline.reflection.understanding_table import understanding_table
from baseline.load_data import json2pd
# from pipeline.reflection.read_table import build_table_json
from baseline.reflection import Reflection
from baseline.outline import Outline
from baseline.narrative import Narration
# from pipeline.reflection.initialize_reflection import initialize_reflection
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
from pipeline.narration.narration import narration

import json
import pandas as pd
import os

OUTPUT_FILE = r"data\output\wo_outline.csv"

if __name__ == "__main__":
    df_input = pd.read_csv("data_input.csv")  # đổi thành df_input

    for idx in range(0,len(df_input)):  # đổi i -> idx
        print(f"Đang xử lý {idx+1}/{len(df_input)}...")
        
        try:
            tables = df_input.iloc[idx]["data"]
            intention = df_input.iloc[idx]["intention"]
            file_path = df_input.iloc[idx]["folder_path"]

            # Reflection
            information_table = understanding_table(intention, tables)
            reflection_obj = Reflection(tables)
            reflection = reflection_obj.reflection()
            information_verified = extract_information(information_table, reflection)

            output = generation_query(information_verified, information_table)
            output = output.strip().replace("```json", "").replace("```", "")
            query_data = json.loads(output)  # đổi data -> query_data

            list_claim = [item["claim"] for item in query_data]
            list_query = [item["sql"] for item in query_data]

            list_output_query = run_query(file_path, tables, list_query)

            list_feedback = []
            list_suggest_fix = []
            reflection_revised = reflection  # đổi tên tránh nhầm

            for j in range(len(list_query)):  # đổi i -> j
                verified = verified_information(information_table, list_claim[j], list_output_query[j])
                verified = verified.strip().replace("```json", "").replace("```", "")
                verified_data = json.loads(verified)
                list_feedback.append(verified_data["feedback"])
                list_suggest_fix.append(verified_data["suggested_fix"])
                reflection_revised = revision_reflection(reflection_revised, list_claim[j], verified_data["feedback"], verified_data["suggested_fix"])
            
            # Outline
                        
            outline = Outline(intention, reflection_revised, tables).outline()

            # Narration
            list_plot = map_plot(outline, tables)
            plot_data = parse_llm_output(list_plot)
            df_plot = llm_output_to_df(plot_data)  # đổi df -> df_plot
            df_plot = plot(file_path, df_plot)

            explain_plot = []
            for j in range(len(df_plot)):  # đổi i -> j
                path_plot = df_plot.iloc[j]["plot_path"]
                if isinstance(path_plot, str):
                    explain_plot.append(explanable_plot(path_plot))
                else:
                    explain_plot.append("")

            df_plot["explanable_plot"] = explain_plot
            df_plot = df_plot.dropna(subset=["plot_path"])
            
            narration_result = narration(outline, df_plot, intention)  # đổi tên tránh trùng function
            
            row = pd.DataFrame([{
                'intention': intention,
                'reflection': reflection_revised,
                'outline': outline,
                'narration': narration_result
            }])

            file_exists = os.path.exists(OUTPUT_FILE)
            row.to_csv(OUTPUT_FILE, index=False, mode='a', header=not file_exists)
            print(f"Đã lưu dòng {idx+1}")

        except Exception as e:
            print(f"Lỗi dòng {idx+1}: {e}")
            import traceback
            traceback.print_exc()
            
            row = pd.DataFrame([{
                'intention': df_input.iloc[idx]["intention"],
                'reflection': 'ERROR',
                'outline': 'ERROR',
                'narration': f'ERROR: {str(e)}'
            }])
            file_exists = os.path.exists(OUTPUT_FILE)
            row.to_csv(OUTPUT_FILE, index=False, mode='a', header=not file_exists)
            continue