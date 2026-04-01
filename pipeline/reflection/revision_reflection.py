from model.gpt import get_llm_response_sys

def revision_reflection(reflection, claim, feedback, suggested_fix):
    system_prompt = """
    You are a precise claim rewriting assistant in a data verification pipeline.

    You are given:
    1. Original reflection (previous generated statement)
    2. Original claim
    3. Feedback from verification step (grounded in SQL output)
    4. Suggested fix (optional corrected version)

    Your task:
    Rewrite the reflection so that it is factually correct based on the feedback.

    RULES:
    - If feedback indicates no issue → keep the reflection unchanged
    - If feedback indicates an error → fix ONLY the incorrect part
    - Prefer using the suggested_fix when provided
    - Do NOT introduce new information
    - Do NOT remove correct parts unnecessarily
    - Keep the sentence natural and fluent

    STYLE:
    - Clear, concise
    - Preserve original meaning as much as possible
    - Ensure all numbers/entities match the corrected data

    OUTPUT FORMAT (JSON):
    {
        "revised_reflection": "..."
    }

    Only return JSON. No extra text. No markdown.
    """

    user_prompt = f"""
    Original Reflection:
    {reflection}

    Original Claim:
    {claim}

    Feedback:
    {feedback}

    Suggested Fix:
    {suggested_fix}

    Rewrite the reflection accordingly.
    """

    return get_llm_response_sys(system_prompt, user_prompt)