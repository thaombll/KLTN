from evaluation.rq1 import evaluation
import pandas as pd

OUTPUT_FILE = r"result_evaluation\RQ1\evaluation_result_baseline_vs_pipeline.csv"

if __name__ == "__main__":
    df = pd.read_csv("data\input\data_input.csv")
    # df_tables = pd.read_csv("data\output\output.csv")

    for i in range(0, len(df)):
        print(f"Đang xử lý {i+1}/{len(df)}...")
        
        try:
            tables = df.iloc[i]["data"]
            intention = df.iloc[i]["intention"]

            baseline = pd.read_csv("data\output\output_baseline.csv").iloc[i]["narration"]
            pipeline = pd.read_csv("data\output\output_our_method.csv").iloc[i]["narration"]
            result_evaluation = evaluation(intention, tables, baseline, pipeline)
    
            row = pd.DataFrame([{
                'intention': intention,
                'baseline_vs_pipeline': result_evaluation
            }])

        except Exception as e:
            print(f"Lỗi dòng {i+1}: {e}")
            row = pd.DataFrame([{
                'intention': df.iloc[i]["intention"],
                'baseline_vs_pipeline': f'ERROR: {str(e)}'
            }])

        file_exists = os.path.exists(OUTPUT_FILE)
        row.to_csv(OUTPUT_FILE, index=False, mode='a', header=not file_exists)
        print(f"Đã lưu dòng {i+1}")