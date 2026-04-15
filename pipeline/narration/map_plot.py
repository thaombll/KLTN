from model.gpt import get_llm_response_sys
import json


def map_plot(outline, tables):
    system_prompt = """
You are an expert data analyst and visualization planner.

Your task is to convert an analytical outline into executable plotting instructions.

You MUST output configurations that can be directly used to call plotting functions.

---

AVAILABLE PLOT FUNCTIONS:

1. plot_bar(x, y, title, xlabel, ylabel)
2. plot_trend(x, y, title, xlabel, ylabel)
3. plot_scatter(x, y, title, xlabel, ylabel)
4. plot_bubble(x, y, size, title, xlabel, ylabel)
5. plot_bar_line(x, bar_values, line_values, title, xlabel, ylabel_bar, ylabel_line)

---

DATA TYPE DETECTION:

Infer column types from tables:

- numeric → numbers (e.g., 100, -50, 0.3, 10%)
- categorical → text (e.g., Country, Positive/Negative)
- time → year, quarter, date

---

COLUMN VALIDATION RULE (CRITICAL):

- You MUST ONLY use column names EXACTLY as they appear in tables
- DO NOT rename columns
- DO NOT invent columns (e.g., "Profit" if not present)
- If required data does not exist → choose another valid column or return "none"

---

CHART SELECTION RULES (STRICT PRIORITY):

1. SCATTER (HIGHEST PRIORITY):
- Use when TWO numeric columns exist
- x = numeric
- y = numeric

- If a categorical column exists:
  → assign it to "color"
  → DO NOT use it as axis

- DO NOT downgrade to bar if scatter is valid

---

2. TREND:
- x = time
- y = numeric

---

3. BAR:
- x = categorical
- y = numeric
- Use ONLY when scatter is NOT possible

---

4. BUBBLE:
- x = numeric
- y = numeric
- size = numeric

---

5. BAR_LINE:
- x = shared category/time
- two numeric series

---

COLOR SELECTION RULE:

- Prefer categorical columns with SMALL number of unique values (2–5)
- Avoid high-cardinality columns (e.g., Country)
- Prefer meaningful grouping columns (e.g., Positive/Negative)

---

WIDE TABLE RULE:

If columns are like 2011, 2012, 2013:
→ treat as time series
→ x = year
→ y = values

---

VALIDATION RULES:

- NEVER use categorical columns as x/y in scatter
- ALWAYS prefer scatter if numeric-numeric exists
- NEVER hallucinate columns
- Ensure mapping is executable

---

OUTPUT FORMAT (STRICT JSON):

[
{
    "section": "...",

    "plot_type": "bar | trend | scatter | bubble | bar_line | none",

    "table_name": "...",

    "columns_used": ["col1", "col2", "..."],

    "plot_params": {
        "x": "...",
        "y": "...",
        "size": "...",
        "bar_values": "...",
        "line_values": "...",
        "color": "..."
    },

    "labels": {
        "title": "...",
        "xlabel": "...",
        "ylabel": "...",
        "ylabel_bar": "...",
        "ylabel_line": "..."
    },

    "reason": "...",
    "no_plot": false
}
]
"""

    user_prompt = f"""
### OUTLINE:
{outline}

### TABLES:
{tables}

### TASK:

For EACH section:

1. Identify intent:
   - comparison
   - trend
   - relationship
   - distribution

2. Detect column types (numeric / categorical / time)

3. Select BEST chart using STRICT PRIORITY RULES

4. Provide FULL plotting parameters

IMPORTANT:

- If TWO numeric columns exist:
  → ALWAYS use scatter

- If a categorical column exists:
  → use it as "color" (NOT axis)

- NEVER use high-cardinality columns (e.g., Country) as color

- DO NOT invent column names

- If cannot plot → return plot_type = "none"

Return ONLY JSON.
"""
    return get_llm_response_sys(system_prompt, user_prompt)