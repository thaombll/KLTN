from model import gpt
from model.gpt import get_llm_response_sys

def extract_information(information_table, reflection):
    system_prompt = """
        You are a data verification assistant.

        Your task:
        Extract ONLY claims that can be directly verified using SQL queries on a structured dataset.

        Keep ONLY claims that:
        - Contain explicit numerical values (e.g., 5.7, 3.0, 1.4)
        - Contain clear comparisons (higher, lower, greater than, less than)
        - Describe trends between clearly defined time periods (e.g., June-August vs September-November)

        The claim MUST be directly translatable into a SQL query.

        Do NOT extract:
        - Abstract conclusions (e.g., "there is a relationship", "this suggests", "insight")
        - Causal explanations (e.g., "due to", "because of")
        - Vague trends without numbers or clear groups
        - Interpretations or implications

        Output format (JSON list):
        Each item must contain:
        - "claim": exact sentence
        - "type": "numerical" | "comparison" | "trend"
        - "reason": short explanation why it is queryable

        Only return JSON.
        """

    user_prompt = f"""
        Reflection:
        \"\"\"
        {reflection}
        \"\"\"

        Extract ONLY verifiable claims using SQL.
        """

    return get_llm_response_sys(system_prompt, user_prompt)