from model import gpt
from model.gpt import get_llm_response_sys

def narration(node):
    system_prompt = f"""
    """
    user_prompt = f"""
    """
    return get_llm_response_sys(system_prompt, user_prompt)