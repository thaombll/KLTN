from model.get_llm_response import get_llm_response
from model import gpt
from model.gpt import get_llm_response_sys
import pandas as pd
import os

def evaluation (intention, tables, story_a, story_b):
    system_prompt = f"""
    You are an expert evaluator for data-driven storytelling.
    Your task is to compare two stories generated from the same data and intention.
    You must evaluate objectively based on specific criteria.
    """

    user_prompt = f"""
    ### Task Description:
    You will receive:
    - A user intention representing the overarching theme of the story
    - Tables data used to generate the stories
    - Two model-generated stories (Story A and Story B)
    Ignore any extra white spaces and newlines in the stories. Your task is to evaluate the quality
    of the LLM-generated stories based on the criteria listed below:
    ### Evaluation Criteria:
    1. **Relevance and Informativeness:** The extent to which the data story addresses the given
    user `intention` and provides substantial and useful information.
    2. **Structure and Coherence:** The logical organization such as a linear narrative structure
    (a beginning, a middle and a conclusion), ease of understanding, and connectivity between
    different parts of the data story.
    3. **Visualization Specification Quality:** The visualization specifications defined within
    `<visualization>` tags are well-suited for creating visualizations that enhance the
    understanding of the data.
    4. **Narrative Quality and Insightfulness:** The ability of the narrative to engage the reader,
    provide important insights, and follow the `intention` provided by the user.
    5. **Factual Correctness:** The accuracy of the data and information presented considering the
    input data tables.

    ### Point Allocation Criteria:
    1. For each evaluation criterion, give 1 point to 'Story A' if it is better than 'Story B', or
    vice versa.
    2. If both stories perform equally well in a criterion, give 1 point to both.
    3. Evaluate the stories based on their total points.
    ### Additional Guidelines:
    - Systematically attribute points to `Story A` and `Story B` based on the `Point Allocation
    Criteria`.
    - Make sure total accumulated points for each story is within a range of 1 to 5.
    - Briefly justify your total score, up to 100 words.
    - Avoid any position biases and ensure that the order in which the stories were presented does
    not influence your decision.
    - Do not allow the length of the stories to influence your evaluation.
    - Be as objective as possible.
    - Remember to assess the data story from the perspective of relevance, clarity, coherence,
    informativeness, and factual correctness, taking the plausible gold story as a reference.
    - After providing your explanation, output your final verdict based on the total points each
    story received by strictly following this format: '[[A]]' if the story A is better, '[[B]]' if
    the story B is better, and '[[C]]' for a tie.
    
    ### INPUT:
    {intention}
    ### Tables data:
    {tables}
    ### Story A:
    {story_a}
    ### Story B:
    {story_b}
    """
    return get_llm_response_sys(system_prompt, user_prompt)
