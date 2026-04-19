from __future__ import annotations

from functools import lru_cache

from proposal_builder.helpers import strip_code_fence


class LLMCaller:
    def __init__(self, client, deployment: str) -> None:
        self._client = client
        self._deployment = deployment

    def call(
        self,
        system_prompt: str,
        user_content: str,
        temperature: float = 0.7,
        extra_messages: list[dict] | None = None,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        if extra_messages:
            messages.extend(extra_messages)
        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=messages,
            temperature=temperature,
        )
        return strip_code_fence(response.choices[0].message.content)


@lru_cache(maxsize=1)
def get_llm() -> LLMCaller:
    from config import settings
    from proposal_builder.llm import create_llm
    return LLMCaller(create_llm(settings), settings.AZURE_OPENAI_DEPLOYMENT)
