from evaluation.rq1 import evaluation
import pandas as pd

OUTPUT_FILE = r"result_evaluation\RQ3\pipeline_vs_wo_element.csv"

if __name__ == "__main__":
    df = pd.read_csv("data\input\data_input.csv")
    # df_tables = pd.read_csv("data\output\output.csv")

    for i in range(0, len(df)):
        print(f"Đang xử lý {i+1}/{len(df)}...")
        
        try:
            tables = df.iloc[i]["data"]
            intention = df.iloc[i]["intention"]

            baseline = pd.read_csv("data\output\output_baseline.csv").iloc[i]["narration"]
            wo_reflection = pd.read_csv("data\output\wo_reflection.csv").iloc[i]["narration"]
            wo_outline = pd.read_csv("data\output\wo_outline.csv").iloc[i]["narration"]
            wo_narration = pd.read_csv("data\output\wo_narration.csv").iloc[i]["narration"]

            result_evaluation_wore = evaluation(intention, tables, pipeline, wo_reflection)
            result_evaluation_woou = evaluation(intention, tables, pipeline, wo_outline)
            result_evaluation_wona = evaluation(intention, tables, pipeline, wo_narration)

            row = pd.DataFrame([{
                'intention': intention,
                'pipeline_vs_wo_reflection': result_evaluation_wore,
                'pipeline_vs_wo_outline': result_evaluation_woou,
                'pipeline_vs_wo_narration': result_evaluation_wona
            }])

        except Exception as e:
            print(f"Lỗi dòng {i+1}: {e}")
            row = pd.DataFrame([{
                'intention': intention,
                'pipeline_vs_wo_reflection': f'ERROR: {str(e)}',
                'pipeline_vs_wo_outline': f'ERROR: {str(e)}',
                'pipeline_vs_wo_narration': f'ERROR: {str(e)}'
            }])

        file_exists = os.path.exists(OUTPUT_FILE)
        row.to_csv(OUTPUT_FILE, index=False, mode='a', header=not file_exists)
        print(f"Đã lưu dòng {i+1}")