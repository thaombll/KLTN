import re

def extract_reflection(reflection):
    text = reflection
    text = re.sub(r"```json|```", "", text)
    text = re.sub(r'"revised_reflection"\s*:\s*', '', text)
    text = re.sub(r"[{}]", "", text)
    text = text.replace('"', '')
    text = re.sub(r"\*\*.*?\*\*", "", text)
    text = re.sub(r"-\s*", "", text)
    text = re.sub(r"(\d)\s*\n\s*(\d+%)", r"\1.\2", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"lossmaking", "loss making", text)
    text = re.sub(r"highdiscount", "high discount", text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]