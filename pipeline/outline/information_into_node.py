from model import gpt
from model.gpt import get_llm_response_sys


def information_into_node(result):
    system_prompt = f"""
    You are an expert in data analysis and insight structuring.

    Your task is to convert each sentence into a STRUCTURED INSIGHT NODE.

    Each node MUST follow this schema:

    - fact_type: one of [Value, Difference, Proportion, Trend, Categorization, Distribution, Rank, Association, Extreme, Outlier]
    - measure (mi): the metric (e.g., profit, discount, growth)
    - aggregation (agg): sum, avg, count, etc.
    - space (si): condition or filter (e.g., countries with negative profit)
    - text: the original sentence

    STRICT RULES:
    - Extract structured components from the sentence
    - If missing, infer conservatively (do NOT hallucinate)
    - One sentence → one node (but simplify if needed)
    - Keep consistency across nodes

    SYNTAX TEMPLATES:

    Value:
    "The {{agg}} {{mi}} is {{Vd}} when {{si}}."

    Difference:
    "The difference between {{xi[1]}} and {{xi[2]}} regarding their {{agg}} {{mi}} is {{Vd}} when {{si}}."

    Proportion:
    "The {{xi}} accounts for {{Vd}} of the {{agg}} {{mi}} when {{si}}."

    Trend:
    "The {{agg}} {{mi}} shows a {{Vd}} trend over {{bi}} when {{si}}."

    Categorization:
    "There are {{Vd}} {{bi}} which are {{xi}} when {{si}}."

    Distribution:
    "The distribution of the {{agg}} {{mi}} over {{bi}} when {{si}} highlights {{xi}}."

    Rank:
    "The top {{Vd}} {{bi}} in terms of {{agg}} {{mi}} are {{xi}} when {{si}}."

    Association:
    "The correlation between {{mi[1]}} and {{mi[2]}} is {{Vd}} when {{si}}."

    Extreme:
    "The {{agg}} {{mi}} reaches a {{Vd}} at {{xi}} when {{si}}."

    Outlier:
    "The {{agg}} {{mi}} of {{xi}} is an outlier when {{si}}."

    OUTPUT:
    Return a JSON list of nodes.
    NO explanation.
    """

    user_prompt = f"""
    Sentences:
    {result}

    Convert into structured insight nodes.
    """

    return get_llm_response_sys(system_prompt, user_prompt)