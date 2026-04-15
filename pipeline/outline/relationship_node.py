from model import gpt
from model.gpt import get_llm_response_sys


def build_relationship(node_a, node_b):
    system_prompt = """
You are an expert in causal reasoning and discourse analysis.

Your task is to determine whether a REAL and JUSTIFIABLE relationship exists between TWO nodes.

---------------------
RELATION TYPES
---------------------
- Elaboration: B adds more detail about A (same measure/context)
- Explanation: B explains why A happens
- Cause: B causes A
- Result: B is caused by A
- Condition: B happens under A
- Background: B provides necessary context for A
- Summary: B summarizes A

---------------------
EVALUATION CRITERIA
---------------------
You MUST compare the following dimensions:
- fact_type
- measure (mi)
- space (si)
- focus (xi)

---------------------
VALID RELATION CONDITIONS
---------------------
A relationship is VALID ONLY IF:
1. There is clear overlap OR logical dependency between nodes
2. The relation can be explicitly justified
3. The nodes are NOT about different measures or unrelated contexts

---------------------
STRICT RULES
---------------------
- Only analyze the TWO given nodes
- Return AT MOST ONE relationship
- If NO strong evidence → return []
- If confidence < 90% → return []

---------------------
OUTPUT FORMAT
---------------------
Return ONLY JSON:

[
  {
    "from": "<exact text of node A>",
    "to": "<exact text of node B>",
    "relation": "<type>"
  }
]

OR

[]
"""

    user_prompt = f"""
Node A:
{node_a}

Node B:
{node_b}

Determine whether a valid relationship exists between them.
"""

    return get_llm_response_sys(system_prompt, user_prompt)