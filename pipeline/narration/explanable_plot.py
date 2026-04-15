from model import gpt
from model.get_llm_response_image import llm_response_image

def explanable_plot(path_plot):
    prompt_text = """
    You are an expert data analyst.

    Your task is to analyze the given chart and extract detailed, structured insights.

    ---------------------
    GOAL
    ---------------------
    Understand the chart and describe:

    1. What variables are shown (axes, legend, units)
    2. Key values and patterns
    3. Trends (increase, decrease, stable)
    4. Comparisons (highest, lowest, differences)
    5. Distribution (if applicable)
    6. Outliers or unusual points
    7. Relationships between variables (if visible)

    ---------------------
    IMPORTANT RULES
    ---------------------
    - Be precise with numbers when possible (estimate if needed)
    - Do NOT hallucinate values that are not visible
    - Use approximate language if unsure (e.g., "around", "roughly")
    - Focus on insights, not just description

    ---------------------
    OUTPUT FORMAT
    ---------------------
    Return a list of insight sentences.

    Each sentence should follow analytical style, for example:
    - "The average revenue increases steadily over time."
    - "Product A has significantly higher sales than Product B."
    - "The highest value occurs at X."
    - "There is a strong positive relationship between X and Y."

    Return ONLY a list of sentences.
    """
    
    return llm_response_image(prompt_text, path_plot)