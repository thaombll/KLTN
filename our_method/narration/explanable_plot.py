from model import gpt
from model.get_llm_response_image import llm_response_image

def explanable_plot(path_plot):
    if path_plot is None:
        return None
    
    prompt_text = """
    You are an expert data analyst.

    Your task is to analyze the given chart and extract detailed, structured insights with SPECIFIC numbers.

    ---------------------
    GOAL
    ---------------------
    Analyze the chart and describe with EXACT values:

    1. What variables are shown (axes labels, units, legend items)
    2. Exact or estimated values for key data points on X and Y axes
    3. Trends with specific numbers (e.g., "increased from X to Y between A and B")
    4. Comparisons with exact values (highest, lowest, differences between specific points)
    5. Distribution details (range, concentration of values)
    6. Outliers with their specific X and Y coordinates
    7. Relationships between variables with quantified observations

    ---------------------
    IMPORTANT RULES
    ---------------------
    - ALWAYS include specific numbers from the chart (read axis values carefully)
    - For each data point mentioned, provide both X and Y values
    - Use approximate language only when values are unclear (e.g., "approximately 1,500")
    - Do NOT hallucinate values that are not visible
    - Focus on quantified insights, not vague descriptions

    ---------------------
    OUTPUT FORMAT
    ---------------------
    Return a list of insight sentences with specific numbers.

    Good examples:
    - "Revenue increased from 1,200 in January to 3,500 in June."
    - "Product A (450 units) outsells Product B (120 units) by roughly 3.7x."
    - "The highest value occurs at X=2020 with Y=98,447."
    - "Values range from -18,694 to 9,107 across all categories."

    Return ONLY a list of sentences. No headers, no bullet symbols.
    """
    
    return llm_response_image(prompt_text, path_plot)