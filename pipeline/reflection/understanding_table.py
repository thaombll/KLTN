from model.gpt import get_llm_response_sys

def understanding_table(tables):
    system_prompt = f"""
        
    """

    user_prompt = f"""
       
    """

    return get_llm_response_sys(system_prompt, user_prompt)