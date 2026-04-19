from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FrameworkConfig:
    data_key: str
    prompt_attr: str
    # Header injected before the framework text. None means no separator.
    header: str | None


FRAMEWORK_REGISTRY: dict[str, FrameworkConfig] = {
    "mlops": FrameworkConfig(
        data_key="mlops",
        prompt_attr="MLOPS",
        header=None,
    ),
    "devops": FrameworkConfig(
        data_key="devops",
        prompt_attr="DEVOPS",
        header=(
            "DEVOPS BEST PRACTICES FRAMEWORK\n"
            "Use as reference to enrich Solution Design. Extract and adapt relevant "
            "principles - do not copy verbatim. Integrate naturally using inline bold "
            "subheadings. Adapt to project's technology stack and context."
        ),
    ),
    "llmops": FrameworkConfig(
        data_key="llmops",
        prompt_attr="LLMOPS",
        header=(
            "LLMOPS BEST PRACTICES FRAMEWORK\n"
            "Use as reference to enrich Solution Design. Extract and adapt relevant "
            "principles - do not copy verbatim. Integrate naturally using inline bold "
            "subheadings. Adapt to project's technology stack and context."
        ),
    ),
    "wow": FrameworkConfig(
        data_key="wow",
        prompt_attr="WOW",
        header=(
            "WAYS OF WORKING FRAMEWORK\n"
            "Use as reference to describe the engagement delivery model. Extract and "
            "adapt relevant principles - do not copy verbatim. Integrate naturally "
            "using inline bold subheadings."
        ),
    ),
}


def append_frameworks(content: str, data: dict, prompts) -> str:
    """Append enabled best-practice frameworks to a prompt content string."""
    for cfg in FRAMEWORK_REGISTRY.values():
        if data.get(cfg.data_key) != "Yes":
            continue
        framework_text = getattr(prompts, cfg.prompt_attr)
        if cfg.header:
            content = content + f"\n\n---\n{cfg.header}\n---\n\n" + framework_text
        else:
            content = content + "\n\n" + framework_text
    return content
