from model import gpt
from model.gpt import get_llm_response_sys

def define_outline(list_relationship, list_sentence):
    system_prompt = """
    You are an expert in discourse planning and narrative structuring.

    Your task is to organize a set of insight sentences into a coherent and logical narrative order based on their relationships.

    ---------------------
    INPUT
    ---------------------
    1. A list of sentences
    2. A list of relationships between sentences

    Each relationship has:
    - from
    - to
    - relation type

    ---------------------
    RELATION MEANING (IMPORTANT)
    ---------------------
    Use relation types to determine ordering:

    - Background / Condition:
    → should come BEFORE the target

    - Cause / Explanation:
    → cause comes BEFORE result

    - Result:
    → comes AFTER the cause

    - Elaboration:
    → comes AFTER the main statement

    - Summary:
    → comes AFTER detailed statements

    ---------------------
    GOAL
    ---------------------
    Reorder the sentences into a coherent story that:

    - Starts with context or background
    - Introduces key observations
    - Explains trends or relationships
    - Ends with conclusions or summaries

    ---------------------
    STRICT RULES
    ---------------------
    - Use ONLY the given sentences (do NOT rewrite)
    - Do NOT add new content
    - Each sentence must appear exactly once
    - Preserve original sentence text
    - Ensure logical and natural flow

    ---------------------
    OUTPUT FORMAT
    ---------------------
    Return ONLY a JSON list of ordered sentences:

    [
    "<sentence 1>",
    "<sentence 2>",
    ...
    ]
    """

    user_prompt = f"""
    Sentences:
    {list_sentence}

    Relationships:
    {list_relationship}

    Reorder the sentences into a coherent narrative.
    """

    return get_llm_response_sys(system_prompt, user_prompt)