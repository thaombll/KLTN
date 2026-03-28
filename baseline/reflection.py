from model import gpt
from model.gpt import get_llm_response_sys

class Reflection:
    def __init__(self, tables):
        self.tables = tables

    def initialize_reflection(self):
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

            ### INPUT:\n### Tables:\n{self.tables}\n### OUTPUT:
            '''

        # print("---------------------------------------------------------")
        # print(f'initialize_reflection: {get_llm_response_sys(system_prompt, user_prompt)}')
        return get_llm_response_sys(system_prompt, user_prompt)

    def reflection_verification(self, reflection_int):
        system_prompt = (
            '''As an analytical critic, your role is to meticulously examine the alignment between data presented in tables and the narrative provided in a reflection. 
            Focus on identifying any discrepancies in the details and the overall message conveyed. Consider not just the numbers but also the context and implications of the data.'''
        )

        user_prompt = f"""
            ### Task Description:
            Given the data tables and a reflection corresponding to a data story in the input, your task is the following:
            1. Carefully analyze the data tables and the reflection. Identify any discrepancies or inconsistencies, focusing on numerical data, contextual interpretations, and the reflection’s fidelity to the data. Discrepancies might include but are not limited to incorrect data interpretation, or overlooked details.
            2. Prepare a plan to revise the reflection if needed, and output the revision plan. Otherwise just output: ‘No revision needed’.
            3. The revision plan if needed must coherently and logically relate to the attributes of the data.
            4. Be as specific as possible.

            ### Additional Guidelines:
            - The output must be in plain text and structured in bullet points.
            - Generate the response ‘reflection’ in between two <reflection> tags.

            ### INPUT:\n### Tables:\n{self.tables}\n### Reflection:\n{reflection_int}\n### OUTPUT:
        """
        # print("---------------------------------------------------------")
        # print(f'Reflection_Verification: {get_llm_response_sys(system_prompt, user_prompt)}')
        return get_llm_response_sys(system_prompt, user_prompt)

    def reflection_revision(self, reflection_int, reflection_revision_plan):
        system_prompt = (
            "As an intelligent data analyst and insight extraction specialist, your role is to generate a ‘reflection’ from data tables that must cover every important detail that can be observed in the data tables. Pay attention to small details and nuances as well as any trends or outliers in the given tables."
        )

        user_prompt = f"""
            ### Task Description:
            Given the data tables corresponding to a data story and a revision plan for reflection in the input, your task is the following:
            1. Revise the reflection according to the revision plan. Pay attention to small details and nuances and any trends or outliers in the given tables.
            2. The generated reflection must coherently and logically relate to the attributes of the data.
            3. Be as specific as possible.

            ### Additional Guidelines:
            - The output must be in plain text and structured in bullet points.
            - Generate the response ‘reflection’ in between two <reflection> tags.

            ### INPUT:\n### Tables:\n{self.tables}\n### Previous Reflection:\n{reflection_int}\n### Revision Plan:\n{reflection_revision_plan}\n### OUTPUT:
        """
        print("---------------------------------------------------------")
        print(f'reflection_revision: {get_llm_response_sys(system_prompt, user_prompt)}')
        return get_llm_response_sys(system_prompt, user_prompt)

    def reflection(self):
        reflection_int = self.initialize_reflection()
        reflection_revision_plan = self.reflection_verification(reflection_int)
        final_reflection_int = self.reflection_revision(reflection_int, reflection_revision_plan)
        return final_reflection_int
