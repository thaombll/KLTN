import pandas as pd
import os
from baseline.reflection import Reflection
from baseline.outline import Outline
from baseline.narrative import Narration
from baseline.load_data import json2pd
from model.gpt import token_usage
import time

OUTPUT_FILE = r"data\output\output_baseline.csv"
OUTPUT_RQ2 = r"result_evaluation\RQ2\time_vs_token_baseline.csv"

if __name__ == "__main__":
    df_input = pd.read_csv("data_input.csv")  # đổi thành df_input

    for idx in range(0,len(df_input)):  # đổi i -> idx
        print(f"Đang xử lý {idx+1}/{len(df_input)}...")
        
        time_reflection = 0
        time_outline = 0
        time_narration = 0
        tokens_reflection = 0
        tokens_reflection_input = 0
        tokens_reflection_ouput = 0
        tokens_outline = 0
        tokens_outline_input = 0
        tokens_outline_ouput = 0
        tokens_narration = 0
        tokens_narration_input = 0
        tokens_narration_ouput = 0
        
        try:
            token_usage["prompt_tokens"] = 0
            token_usage["completion_tokens"] = 0
            token_usage["total_tokens"] = 0

            tables = df_input.iloc[idx]["data"]
            intention = df_input.iloc[idx]["intention"]
            file_path = df_input.iloc[idx]["folder_path"]

            start_time = time.time()

            reflection_revised = Reflection(tables).reflection()

            time_reflection = time.time()- start_time

            print("----------------------------------------")
            print(f'time_reflection: {time_reflection}')

            tokens_reflection_input = token_usage["prompt_tokens"]
            tokens_reflection_ouput = token_usage["completion_tokens"]
            tokens_reflection = token_usage["total_tokens"]
            print(f'tokens_reflection_input: {tokens_reflection_input} \n tokens_reflection_ouput: {tokens_reflection_ouput} \n tokens_reflection: {tokens_reflection} \n')


            token_usage["prompt_tokens"] = 0
            token_usage["completion_tokens"] = 0
            token_usage["total_tokens"] = 0

            start_time = time.time()

            outline = Outline(intention, reflection_revised, tables).outline()
            time_outline= time.time()- start_time
            print("----------------------------------------")
            print(f'time_outline: {time_outline}')
            tokens_outline_input = token_usage["prompt_tokens"]
            tokens_outline_ouput = token_usage["completion_tokens"]
            tokens_outline = token_usage["total_tokens"]
            print(f'tokens_outline_input: {tokens_outline_input} \n tokens_outline_ouput: {tokens_outline_ouput} \n tokens_outline: {tokens_outline} \n')

            start_time = time.time()

            token_usage["prompt_tokens"] = 0
            token_usage["completion_tokens"] = 0
            token_usage["total_tokens"] = 0
            
            narration_result = Narration(intention, tables, outline).narration()
            # print(narration_result)
            time_narration= time.time()- start_time
            print("----------------------------------------")
            print(f'time_narration: {time_narration}')
            tokens_narration_input = token_usage["prompt_tokens"]
            tokens_narration_ouput = token_usage["completion_tokens"]
            tokens_narration = token_usage["total_tokens"]
            print(f'tokens_narration_input: {tokens_narration_input} \n tokens_narration_ouput: {tokens_narration_ouput} \n tokens_narration: {tokens_narration} \n')

            row = pd.DataFrame([{
                'intention': intention,
                'reflection': reflection_revised,
                'outline': outline,
                'narration': narration_result
            }])

            file_exists = os.path.exists(OUTPUT_FILE)
            row.to_csv(OUTPUT_FILE, index=False, mode='a', header=not file_exists)
            print(f"Đã lưu dòng {idx+1}")

            row1 = pd.DataFrame([{
                'time_reflection': time_reflection,
                'time_outline': time_outline,
                'time_narration': time_narration,
                'tokens_reflection': tokens_reflection,
                'tokens_outline': tokens_outline,
                'tokens_narration': tokens_narration
            }])
            file_exists = os.path.exists(OUTPUT_RQ2)
            row1.to_csv(OUTPUT_RQ2, index=False, mode='a', header=not file_exists)

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

            row1 = pd.DataFrame([{
                'time_reflection': time_reflection,
                'time_outline': time_outline,
                'time_narration': time_narration,
                'tokens_reflection': tokens_reflection,
                'tokens_outline': tokens_outline,
                'tokens_narration': tokens_narration
            }])

            file_exists = os.path.exists(OUTPUT_RQ2)
            row1.to_csv(OUTPUT_RQ2, index=False, mode='a', header=not file_exists)

            continue
