def read_prompt(prompt_path : str) -> str:
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()
    return prompt
