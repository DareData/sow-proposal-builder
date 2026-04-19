def read_prompt(prompt_path : str) -> str:
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()
    return prompt


def strip_code_fence(text: str) -> str:
    """Remove outer markdown code fences the LLM sometimes wraps its output in."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return text
    newline = stripped.find("\n")
    if newline == -1:
        return text
    inner = stripped[newline + 1:]
    if inner.endswith("```"):
        inner = inner[:-3].rstrip()
    return inner
