from model import gpt
from model.gpt import get_llm_response_sys

class Narration:
    def __init__(self, intention, tables, final_outline_int):
        self.intention = intention
        self.tables = tables
        self.final_outline_int = final_outline_int

    def initialize_narration_prompt(self):
        # NARRATION
        # ======================================== $$Initial Narration with Intent$$ ======================================================
        initial_system_narration_prompt = f'You are an expert at generating engaging data stories. The generated data story should cover every important detail that can be observed in the data tables. Pay attention to small details and nuances as well as any trends or outliers in the given tables.'
        initial_user_narration_prompt = f'''### Task Description:
        Given a outline and the data tables corresponding to a data story in the input, you have the following tasks:
        1. Follow the outline rigorously to create a "data story" that will be highly informative and engaging to the audience.
        2. Highlight key statistics that are critical to understanding the theme. Explain these elements in a way that balances technical accuracy with accessibility, ensuring that your narrative is approachable for a non-specialist audience while still offering depth for those more familiar with the subject matter. Think about the narrative flow and how each piece of data contributes to the overall story arc.
        3. The overarching theme, denoted as "{self.intention}", should be the narrative’s backbone. Ensure that this theme resonates throughout the story, tying together different data points and insights into a coherent whole.
        4. In the outline, if it is mentioned to include a visualization, then include a ‘visualization placeholder’. Each visualization placeholder should also suggest a narrative element that the visualization supports or explains.
        5. Ensure that each portion of text in the story is in between two <text> tags.
        6. The visualization placeholder must contain necessary information about the visualization, such as:
        - chart title
        - chart type
        - x-axis and y-axis labels
        - x-axis data values and y-axis data values, etc.
        7. The visualizations must be put in between two <visualization> tags.
        8. Finally, make sure that the story is engaging to the audience.
        
        ### Additional Guidelines:
        - The output must be in plain text.
        - Generate the response narration in between two <narration> tags.
        
        ### INPUT:\n### Tables:\n{self.tables}\n### Outline:\n{self.final_outline_int}\n### OUTPUT:
        '''
        return get_llm_response_sys(initial_system_narration_prompt, initial_user_narration_prompt)
    
    
    def narration_verification_prompt(self, narration_int):
        # ======================================== $$Narration Verification with Intent$$ =====================================================
        system_narration_verification_prompt = f'You are an intelligent critic, whose job is to identify inconsistencies between data presented in data tables, and an outline and a data story. Pay attention to small details and nuances as well as any trends or outliers in the given tables.'
        user_narration_verification_prompt = f'''### Task Description:
        Given the outline, the data tables and a data story in the input, you have the following tasks:
        1. Examine the data presented in the tables, the story’s outline, and the narrative itself. Look for discrepancies, inaccuracies, or any details that do not align.
        2. Provide a step-by-step analysis, highlighting specific data points and narrative elements that contribute to these inconsistencies.
        3. Make sure the story fully aligns with the intention or the main theme: "{self.intention}"
        4. Based on your analysis, draft a revision plan to refine the data story. Your plan should address identified inconsistencies and enhance theme alignment. Otherwise output: ‘No revision needed’.
        5. The output must be coherent, logically structured, and detailed, aiming for constructive feedback that enhances the data story’s impact.
        
        ### Additional Guidelines:
        - The output must be in plain text and in bullet points.
        - Generate the response narration in between two <narration> tags.
        
        ### INPUT:\n### Tables:\n{self.tables}\n### Outline:\n{self.final_outline_int}\n### Data Story:\n{narration_int}\n### OUTPUT:
        '''
        return get_llm_response_sys(system_narration_verification_prompt, user_narration_verification_prompt)

    def narration_revision_prompt(self, narration_int, narration_int_revision_plan):
    # ======================================== $$Narration Revision with Intent$$ =========================================================
        system_narration_revision_prompt = f'You are an expert at generating engaging data stories. The generated data story will cover every important detail that can be observed in the data tables. Pay attention to small details and nuances as well as any trends or outliers in the given tables.'
        user_narration_revision_prompt = f'''### Task Description:
        Given the data tables, the outline, the revision plan, and the data story in the input, your task is the following:
        1. Revise the data story according to the revision plan. Use the provided outline as your guide, adjusting the narrative according to the revision plan.
        2. The overarching theme, denoted as "{self.intention}", should be the narrative’s backbone.
        3. Ensure that this theme resonates throughout the story, tying together different data points and insights into a coherent whole.
        4. In the outline, if it is mentioned to include a visualization, then include a ‘visualization placeholder’. Each visualization placeholder should also suggest a narrative element that the visualization supports or explains.
        5. Ensure that each portion of text in the story is in between two <text> tags.
        6. The visualization placeholder must contain necessary information about the visualization, such as:
        - chart title
        - chart type
        - x-axis and y-axis labels
        - x-axis data values and y-axis data values, etc.
        7. The visualizations must be put in between two <visualization> tags.
        8. Finally, make sure that the story is engaging to the audience.
        
        ### Additional Guidelines:
        - The output must be in plain text.
        - Generate the response narration in between two <narration> tags.
        
        ### INPUT:\n### Tables:\n{self.tables}\n### Outline:\n{self.final_outline_int}\n### Previous Data Story:\n{narration_int}\n### Revision Plan:\n{narration_int_revision_plan}\n### OUTPUT:
        '''
        print("---------------------------------------------------------")
        print(f'narration_revision: {get_llm_response_sys(system_narration_revision_prompt, user_narration_revision_prompt)}')
        return get_llm_response_sys(system_narration_revision_prompt, user_narration_revision_prompt)

    def narration(self):
        narration_int = self.initialize_narration_prompt()
        narration_int_revision_plan = self.narration_verification_prompt(narration_int)
        final_narration_int = self.narration_revision_prompt(narration_int, narration_int_revision_plan)
        return final_narration_int
