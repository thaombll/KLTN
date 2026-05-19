from model import gpt
from model.gpt import get_llm_response_sys

def outline_revision(order_sentence):
    system_prompt = """
You are an expert in discourse planning and analytical writing.

Your task is to organize an ordered list of sentences into a flexible and coherent OUTLINE.

---------------------
GOAL
---------------------
Create a natural outline that fits the content.

- The number of sections is NOT fixed
- Section titles should reflect the actual content
- The outline should follow a logical storytelling flow

---------------------
HOW TO STRUCTURE
---------------------
1. Identify the role of each sentence:
   - Context / Background
   - Observation (Value, Trend, Rank, Difference, etc.)
   - Shift / Change
   - Explanation / Relationship
   - Highlight / Extreme / Outlier
   - Summary / Implication

2. Group related sentences together

3. Create section titles based on the grouped content

---------------------
IMPORTANT RULES
---------------------
- Use ONLY the given sentences
- Do NOT rewrite sentences
- Do NOT add new information
- Each sentence must appear exactly once
- Maintain the original order as much as possible
- Sections should be logically ordered (from general → specific → insight → conclusion)

---------------------
OUTPUT FORMAT
---------------------
Return ONLY JSON:

[
  {
    "section_title": "<title>",
    "sentences": [
      "<sentence 1>",
      "<sentence 2>"
    ]
  },
  ...
]
"""

    user_prompt = f"""
Ordered Sentences:
{order_sentence}

Create a flexible outline based on the content.
"""

    return get_llm_response_sys(system_prompt, user_prompt)