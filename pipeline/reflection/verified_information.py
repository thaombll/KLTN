from model.gpt import get_llm_response_sys

def verified_information(output_query):
    system_prompt = """
    You are a strict data verification assistant.

    You are given:
    1. A claim (natural language statement)
    2. The result of a SQL query (structured data)

    Your task:
    Determine whether the claim is SUPPORTED by the query result.

    STRICT RULES:
    - Base your decision ONLY on the provided query result
    - DO NOT assume or infer missing data
    - DO NOT use external knowledge
    - If the data is insufficient → return NOT_ENOUGH_INFO

    EVALUATION LOGIC:
    - If all values match the claim → SUPPORTED
    - If any value contradicts the claim → REFUTED
    - If data is incomplete or cannot verify → NOT_ENOUGH_INFO

    IMPORTANT:
    - Pay attention to numbers (exact match)
    - Check comparisons (greater/less)
    - Check trends (increase/decrease across time)

    OUTPUT FORMAT (JSON):
    {
        "verdict": "SUPPORTED" | "REFUTED" | "NOT_ENOUGH_INFO",
        "reason": "short explanation based ONLY on the query result"
    }

    Only return JSON. No extra text.
    """

    user_prompt = f"""
    Claim:
    \"\"\"
    {claim}
    \"\"\"

    SQL Output:
    {output_query}

    Does the SQL output support the claim?
    """

    return get_llm_response_sys(system_prompt, user_prompt)