import pandas as pd
from baseline.load_data import json2pd
from baseline.reflection import Reflection
from baseline.outline import Outline
from baseline.narrative import Narration

def baseline_storytelling(tables, intention):
    reflection_obj = Reflection(tables)
    reflection = reflection_obj.reflection()

    outline_obj = Outline(intention, reflection, tables)
    outline = outline_obj.outline()

    narrative_obj = Narration(intention, tables, outline)
    narrative = narrative_obj.narration()
    return narrative

if __name__ == "__main__":
    file_path = "data\\Test\\Pew\\pew_test.json"
    test_df = json2pd(file_path)
    intention = test_df.iloc[0]["intent"]['0']
    res = test_df.iloc[0]["paragraph_table_pair"]['0']
    tables = ''
  
    for x, item in enumerate(res):
        tables += f'### Table_{x}:\n{item["table"]}\n'

    # baseline_storytelling(tables, intention)

    # file_path = "data\\Test\\Tableau\\tableau_test.json"

    # print(intention)

    # print(res)

    # print("--------------------------------------------------------")
    # print(f'Intention: {intention}')
    print("--------------------------------------------------------")
    print(f'Table: \n {tables}')
