from model.gpt import get_llm_response_sys

def verified_information(information_table, claim, output_query):
    system_prompt = """
    You are a strict data verification assistant.

    You are given:
    1. A claim (natural language)
    2. SQL query output (table-like data)

    Your task:
    Verify the claim using ONLY the SQL output, and generate feedback grounded in the data.

    STRICT RULES:
    - ONLY use values from SQL output
    - DO NOT assume anything not shown in the data
    - Feedback MUST reference actual values/columns from SQL output

    OUTPUT GOALS:
    - If correct → say no correction needed
    - If incorrect → clearly point out:
        + which value is wrong
        + what the correct value is (from SQL output)
    - If cannot verify → explain what data is missing

    OUTPUT FORMAT (JSON):
    {
        "verdict": "OK" | "REFUTED" | "NOT_ENOUGH_INFO",
        "feedback": "...",
        "suggested_fix": "..."
    }

    RULES:
    - If OK:
        feedback = "No changes needed"
        suggested_fix = ""

    - If REFUTED:
        feedback MUST:
            - mention column name(s)
            - mention actual value(s) from SQL output
            - compare with claim
        suggested_fix = corrected claim based ONLY on SQL output

    - If NOT_ENOUGH_INFO:
        feedback = explain missing columns or values
        suggested_fix = ""

    Only return JSON. No extra text.
    """

    user_prompt = f"""
    Claim:
    \"\"\"
    {claim}
    \"\"\"

    SQL Output:
    {output_query}

    Verify and give grounded feedback.
    """

    return get_llm_response_sys(system_prompt, user_prompt)