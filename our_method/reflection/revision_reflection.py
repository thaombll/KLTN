from model.gpt import get_llm_response_sys

def revision_reflection(reflection, claim, feedback, suggested_fix):
    system_prompt = """
    You are a precise reflection rewriting assistant in a data verification pipeline.

    You are given:
    1. Original reflection (list of verifiable facts)
    2. Original claim that was verified
    3. Feedback from verification step (grounded in SQL output)
    4. Suggested fix (optional corrected version)

    Your task:
    Rewrite the ENTIRE reflection so that:
    1. Incorrect facts are fixed based on feedback
    2. Other facts that may be affected by the correction are also updated accordingly
    3. New insights that can be derived from the corrected facts are added if relevant

    RULES:
    - If feedback indicates no issue → keep the reflection unchanged
    - If feedback indicates an error → fix the incorrect part using suggested_fix
    - After fixing, re-examine OTHER bullet points that may be logically affected
    - You MAY add new verifiable insights derived from the corrected information
    - Do NOT introduce information that cannot be derived from the corrected facts
    - Do NOT remove correct and relevant bullet points
    - All facts must still be verifiable against the data

    STYLE:
    - Clear, concise bullet points
    - All numbers/entities must match corrected data
    - Preserve original structure as much as possible

    OUTPUT FORMAT (JSON):
    {
        "revised_reflection": "..."
    }

    Only return JSON. No extra text. No markdown.
    """

    user_prompt = f"""
    Original Reflection:
    {reflection}

    Original Claim that was verified:
    {claim}

    Feedback from verification:
    {feedback}

    Suggested Fix:
    {suggested_fix}

    Rewrite the full reflection based on the feedback and re-derive any affected insights.
    """

    return get_llm_response_sys(system_prompt, user_prompt)