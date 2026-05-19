from model import gpt
from model.gpt import get_llm_response_sys


def build_relationship(node_a, node_b):
    system_prompt = """
  You are an expert in data analysis, causal reasoning, and discourse structure.

  Your task is to determine whether a meaningful and justifiable relationship exists between TWO insight nodes.

  ---------------------
  RELATION TYPES
  ---------------------
  - Elaboration: B adds more detail or specification about A (same metric/context)
  - Explanation: B explains why A happens (can involve different but related measures)
  - Cause: B directly causes A
  - Result: B is a consequence of A
  - Condition: B occurs under the condition described in A
  - Background: B provides contextual information for A
  - Summary: B summarizes or generalizes A

  ---------------------
  NODE STRUCTURE
  ---------------------
  Each node contains:
  - fact_type
  - measure (mi)
  - aggregation (agg)
  - space (si)
  - text

  ---------------------
  RELATION GUIDELINES
  ---------------------
  Use the following rules to infer relationships:

  1. SAME METRIC (mi):
    - If nodes share the same measure (mi) and similar space (si):
      → likely Elaboration or Summary

  2. SAME CONTEXT (si):
    - If nodes are under the same condition but different aspects:
      → Elaboration or Background

  3. TREND + VALUE:
    - If one node describes a Trend and another gives a Value of same metric:
      → Elaboration

  4. DIFFERENT BUT RELATED METRICS:
    - If measures are logically connected (e.g., discount → sales, cost → profit):
      → Explanation or Association

  5. CONTEXT → METRIC:
    - If one node defines condition (si) and the other describes metric:
      → Condition or Background

  6. GENERAL ↔ SPECIFIC:
    - If one node is broader and the other more specific:
      → Elaboration or Summary

  ---------------------
  VALIDITY CONDITIONS
  ---------------------
  A relationship is VALID if:
  - There is semantic overlap OR logical dependency
  - The relation can be reasonably inferred from the node texts
  - The nodes are not completely unrelated

  ---------------------
  IMPORTANT NOTES
  ---------------------
  - Do NOT be overly conservative
  - If a reasonable relationship exists, return it
  - Only return [] if nodes are clearly unrelated
  - Return ONLY ONE best relation

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