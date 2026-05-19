from model import gpt
from model.gpt import get_llm_response_sys

def reflection(tables):
    system_prompt = (
        "As an intelligent data analyst and insight extraction specialist, your role is to generate a ‘reflection’ from data tables that must cover every important detail that can be observed in the data tables. Pay attention to small details and nuances as well as any trends or outliers in the given tables."
    )

    user_prompt = f'''### Task Description:
            Given the data tables corresponding to a data story in the input, your task is the following:
            1. Generate a coherent ‘reflection’ on the data tables given in the input, in bullet points. Here, ‘reflection’ is defined as the systematic examination and interpretation of data tables to narrate a coherent story, involving a comprehensive understanding of the data structure, identification of key variables, analysis of data distribution and trends, and understanding of the data’s broader context.
            2. Identify and discuss the most impactful insights from the data tables. Focus on elements that significantly influence the narrative or findings, such as critical trends, notable patterns, and significant outliers.
            3. Determine the importance of details based on their relevance to the overall story, potential implications, and their statistical significance.
            4. Explain how different attributes of the data tables are interconnected. Highlight any causal relationships, correlations, or patterns that emerge from the data.
            5. Discuss any observed trends or outliers, explaining their potential implications or causes.

            ### Additional Guidelines:
            - The output must be in plain text and structured in bullet points.
            - Generate the response ‘reflection’ in between two <reflection> tags.

            ### INPUT:\n### Tables:\n{tables}\n### OUTPUT:
        l'''

    return get_llm_response_sys(system_prompt, user_prompt)
 