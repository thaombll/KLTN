from model import gpt
from model.gpt import get_llm_response_sys

class Outline:
    def __init__(self, intention, reflection, tables):
        self.intention = intention
        self.reflection = reflection
        self.tables = tables

    def initialize_outline_prompt(self):
        system_prompt = (
            "You are an expert at generating outlines for data stories. The generated outline should cover every important detail that can be observed in the data tables. Pay attention to small details and nuances as well as any trends or outliers in the given tables."
        )

        user_prompt = f"""
            ### Task Description:
            Given a reflection and the data tables corresponding to a data story in the input, you have the following tasks:
            1. Generate an outline of the story following a linear narrative structure considering the reflection and the data presented in the tables. A linear narrative structure is defined as the narrative structure that contain a start, a middle, and an end. Think of it as setting the scene, unveiling the adventure, and wrapping up with a satisfying conclusion.
            2. Each of the points in the outlinebreak it down into smaller points that spotlight specific aspects of the data. This could include: significant figures or patterns, noteworthy exceptions or deviations, comparisons or changes over time. Add instructions for visualizations, i.e., charts, where necessary.
            3. The data story’s overarching theme should focus on "{self.intention}". Make sure this sentiment is consistent throughout the outline.
            4. Remember, the essence of a compelling data story is not just in the numbers but in how you tell the tale, so inclusion of visualization instruction is of utmost importance.
            5. Be specific, be clear, and most importantly, be engaging. The generated outline must coherently and logically relate to the attributes of the data. Be as specific as possible.

            ### Additional Guidelines:
            - The output must be in plain text and structured in bullet points.
            - Generate the response outline in between two <outline> tags.

            ### INPUT:\n### Tables:\n{self.tables}\n### Reflection:\n{self.reflection}\n### OUTPUT:
        """
        return get_llm_response_sys(system_prompt, user_prompt)

    def outline_verification_prompt(self, outline_int):
        # ============================== $$Outline Consistency Check$$ ==============================
        system_prompt = (
            "You are an intelligent critic, whose job is to identify inconsistencies between data presented in data tables, and a reflection and an outline. Pay attention to small details and nuances as well as any trends or outliers in the given tables."
        )

        user_prompt = f"""
            ### Task Description:
            Given the data tables, a reflection and an outline corresponding to a data story in the input, your task is the following:
            1. Identify inconsistencies between the data presented in the tables, the reflection and the outline.
            2. Make sure the revision plan is consistent with the intention or the main theme of the story: "{self.intention}"
            3. Prepare a plan to revise the outline if needed, and output the revision plan. Otherwise just output: ‘No revision needed’.
            4. The revision plan must coherently and logically relate to the attributes of the data. Be as specific as possible.

            ### Additional Guidelines:
            - The output must be in plain text and structured in bullet points.
            - Generate the response outline in between two <outline> tags.

            ### INPUT:\n### Tables:\n{self.tables}\n### Reflection:\n{self.reflection}\n### Outline:\n{outline_int}\n### OUTPUT:
        """
        
        return get_llm_response_sys(system_prompt, user_prompt)

    def outline_revision_prompt(self, outline_int, outline_int_revision_plan):
        # ============================== $$Outline Revision$$ ==============================
        system_prompt = (
            "You are an expert at generating outlines for data stories. The generated outline should cover every important detail that can be observed in the data tables. Pay attention to small details and nuances as well as any trends or outliers in the given tables."
        )

        user_prompt = f"""
            ### Task Description:
            Given the data tables, the revision plan and the outline corresponding to a data story in the input, your task is the following:
            1. Apply the changes suggested in the revision plan to the existing outline.
            2. Ensure Theme Consistency: The data story’s overarching theme, defined as "{self.intention}", should be clearly reflected throughout the revised outline.
            3. Adjust the narrative flow to keep this theme central to the story, ensuring that each section contributes meaningfully to the theme.
            4. The revised outline should be detailed in plain text, with each bullet point clearly articulating the specific aspect of the data story it addresses.
            5. Use sub-bullet points to elaborate on complex points or to incorporate multiple data insights.

            ### Additional Guidelines:
            - The output must be in plain text and structured in bullet points.
            - Generate the response outline in between two <outline> tags.

            ### INPUT:\n### Tables:\n{self.tables}\n### Previous Outline:\n{outline_int}\n### Revision Plan:\n{outline_int_revision_plan}\n### OUTPUT:
            """

        print("---------------------------------------------------------")
        print(f'outline_revision: {get_llm_response_sys(system_prompt, user_prompt)}')
        return get_llm_response_sys(system_prompt, user_prompt)

    def outline(self):
        outline_int = self.initialize_outline_prompt()
        outline_int_revision_plan = self.outline_verification_prompt(outline_int)
        final_outline_int = self.outline_revision_prompt(outline_int, outline_int_revision_plan)
        return final_outline_int
