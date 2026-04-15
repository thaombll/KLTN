from model.gpt import get_llm_response_sys
import json


def narration(outline, df, intention="Data Analysis Story"):
    system_prompt = """
    You are an expert data storyteller.

    Your task is to transform structured analytical insights and visualization explanations into a coherent, engaging narrative.

    You MUST integrate:
    - Outline structure
    - Visualization information
    - Plot explanations

    ---

    RULES:

    1. Follow the OUTLINE strictly (section by section)

    2. For each section:
    - Write a clear and engaging explanation
    - Use insights from the data and plot explanations

    3. If a section has a visualization:
    - Insert a <visualization> block AFTER the text
    - Use the provided plot metadata (DO NOT invent)

    4. Each text block must be inside:
    <text> ... </text>

    5. Each visualization must be inside:
    <visualization> ... </visualization>

    6. DO NOT create new charts
    → ONLY use given plots

    7. Make the story:
    - logical
    - insightful
    - engaging

    ---

    OUTPUT FORMAT:

    <narration>

    <section>
    <text>...</text>
    <visualization>...</visualization>
    </section>

    </narration>
    """

    df_json = df.to_dict(orient="records")

    user_prompt = f"""
    ### OUTLINE:
    {outline}

    ### VISUALIZATION DATA (from dataframe):
    Each item contains:
    - section
    - plot_type
    - plot parameters
    - labels
    - explanable_plot (description of chart)

    {df_json}

    ### INTENTION:
    {intention}

    ---

    ### TASK:

    Generate a full data story:

    - Follow the outline
    - For each section:
        + Write explanation using explanable_plot
        + Integrate insights naturally

    - If plot exists (plot_type != "none"):
        → insert <visualization> block

    Visualization block should include:
    - title
    - chart type
    - axes
    - short explanation of what it shows

    - DO NOT repeat raw JSON
    - DO NOT hallucinate data

    ---

    ### OUTPUT:
    """

    return get_llm_response_sys(system_prompt, user_prompt)