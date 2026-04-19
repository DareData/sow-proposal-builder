"""
Static (non-LLM) proposal sections loaded from templates/.

All functions are pure: same inputs always produce the same output with no
side effects. They can be unit-tested without any LLM credentials.
"""
from __future__ import annotations


def get_pricing(project_type: str, language: str) -> str:
    from config import templates
    if project_type == "Gen-OS":
        key = "PRICING_GEN_OS_PT" if language == "Portuguese" else "PRICING_GEN_OS_EN"
    else:
        key = "PRICING_STANDARD_PT" if language == "Portuguese" else "PRICING_STANDARD_EN"
    return getattr(templates, key).strip()


def get_sifide() -> str:
    from config import templates
    return templates.SIFIDE_PT.strip()


def get_work_agreement(project_type: str, language: str, special_conditions: str = "") -> str:
    from config import templates
    if language == "Portuguese":
        payment_terms = templates.PAYMENT_TERMS_PT[project_type]
        text = templates.WORK_AGREEMENT_PT.replace("{{PAYMENT_TERMS}}", payment_terms)
    else:
        payment_terms = templates.PAYMENT_TERMS_EN[project_type]
        text = templates.WORK_AGREEMENT_EN.replace("{{PAYMENT_TERMS}}", payment_terms)

    special = special_conditions.strip()
    if special:
        label = "**Condições Especiais**" if language == "Portuguese" else "**Special Conditions**"
        text = text.strip() + f"\n\n{label}\n\n{special}"

    return text.strip()
