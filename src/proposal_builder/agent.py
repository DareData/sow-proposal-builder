"""
Proposal generation orchestrator.

Two-phase pattern inside generate_proposal():
  Phase 1 — LLM sections computed in dependency order
             (executive_summary must run after project_desc; all others are independent)
  Phase 2 — Sections assembled in reader/document order
             (which differs from computation order)

Static sections (pricing, SIFIDE, work agreement) involve no LLM calls and are
handled by static_sections.py — edit those files under proposal_builder/templates/.
"""
from __future__ import annotations

import json

from pathlib import Path

from config import prompts
from proposal_builder.case_parser import parse_cases, build_compact_catalog
from proposal_builder.frameworks import append_frameworks
from proposal_builder.llm_caller import get_llm
from proposal_builder.static_sections import get_pricing, get_sifide, get_work_agreement

_STORYTELLING_PATH = Path(__file__).resolve().parent.parent.parent / "Project_Storytelling.md"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_proposal(data: dict) -> str:
    llm = get_llm()

    # Phase 1: LLM sections (dependency order)
    project_desc = _project_description(data, llm)
    timeline = _timeline_planning(data, llm)
    team = _daredata_team(data, llm)
    requirements = _requirements(data, llm)
    experience = _daredata_experience(data, project_desc, llm)
    exec_summary = _executive_summary(data, project_desc, llm)
    exec_presentation = _exec_summary_presentation(data, project_desc, llm)

    # Phase 2: static sections
    pricing = get_pricing(data["project_type"], data["language"])
    sifide = get_sifide() if data["language"] == "Portuguese" else ""
    work_agreement = get_work_agreement(
        data["project_type"], data["language"], data.get("special_conditions", "")
    )

    # Phase 3: assemble in document order, dropping empty sections
    sections = [
        exec_summary,
        project_desc,
        timeline,
        experience,
        team,
        requirements,
        pricing,
        sifide,
        work_agreement,
        exec_presentation,
    ]
    return "\n\n".join(s.strip() for s in sections if s.strip())


# ---------------------------------------------------------------------------
# LLM section generators (private)
# ---------------------------------------------------------------------------

def _executive_summary(data: dict, description: str, llm) -> str:
    payload = {"language": data["language"], "project description": description}
    return llm.call(
        prompts.SYSTEM_PROMPT,
        prompts.EXECUTIVE_SUMMARY + json.dumps(payload),
        temperature=0.5,
    )


def _project_description(data: dict, llm) -> str:
    fields = ("client_name", "language", "technology_focus", "general_description")
    content = prompts.PROJECT_DESCRIPTION + json.dumps(
        {k: v for k, v in data.items() if k in fields}
    )
    content = append_frameworks(content, data, prompts)

    extra = None
    if data.get("extended_description"):
        extra = [{"role": "user", "content": (
            "Please provide an extended, more comprehensive project description. "
            "The description should be thorough and substantial, suitable for a "
            "large-scale client project."
        )}]

    result = llm.call(prompts.SYSTEM_PROMPT, content, extra_messages=extra)

    if data["project_type"] == "GenOS":
        gen_os_template = _build_gen_os_template(data, prompts)
        adjustment_system = (
            "Adjust the following subsection"
            "\n\n###############\n\n"
            + gen_os_template
            + "\n\n###############\n\n"
            "by simply adding a couple of sentences relating it to the project "
            "the user will tell you."
        )
        adjustment = llm.call(adjustment_system, result)
        result = result + "\n" + gen_os_template + adjustment

    return result


def _timeline_planning(data: dict, llm) -> str:
    fields = ("language", "planning", "client_name")
    payload = {k: v for k, v in data.items() if k in fields}
    return llm.call(prompts.SYSTEM_PROMPT, prompts.TIMELINE_AND_PLANNING + json.dumps(payload))


def _daredata_team(data: dict, llm) -> str:
    fields = ("client_name", "language", "daredata_team", "project_type")
    payload = {k: v for k, v in data.items() if k in fields}
    return llm.call(prompts.SYSTEM_PROMPT, prompts.DAREDATA_TEAM + json.dumps(payload))


def _requirements(data: dict, llm) -> str:
    if not data.get("client_expectations", "").strip():
        return ""
    fields = ("client_name", "language", "client_expectations")
    payload = {k: v for k, v in data.items() if k in fields}
    return llm.call(prompts.SYSTEM_PROMPT, prompts.REQUIREMENTS_AND_PRICING + json.dumps(payload))


def _build_gen_os_template(data: dict, prompts) -> str:
    is_pt = data["language"] == "Portuguese"
    parts = []
    if data.get("gen_os_assistant"):
        parts.append(prompts.GEN_OS_ASSISTANT_PT if is_pt else prompts.GEN_OS_ASSISTANT)
    if data.get("gen_os_supervisor"):
        parts.append(prompts.GEN_OS_SUPERVISOR_PT if is_pt else prompts.GEN_OS_SUPERVISOR)
    if data.get("gen_os_service"):
        parts.append(prompts.GEN_OS_SERVICE_PT if is_pt else prompts.GEN_OS_SERVICE)
    parts.append(prompts.GEN_OS_PLATFORM_PT if is_pt else prompts.GEN_OS_PLATFORM)
    return "\n\n".join(p for p in parts if p.strip())


def _daredata_experience(data: dict, description: str, llm) -> str:
    if not _STORYTELLING_PATH.exists():
        return ""
    cases = parse_cases(_STORYTELLING_PATH)
    if not cases:
        return ""
    catalog = build_compact_catalog(cases)
    user_content = (
        f"Language: {data['language']}\n\n"
        f"PROJECT DESCRIPTION:\n{description}\n\n"
        f"CASE CATALOG:\n{catalog}"
    )
    return llm.call(prompts.SYSTEM_PROMPT, prompts.DAREDATA_EXPERIENCE + user_content)


def _exec_summary_presentation(data: dict, description: str, llm) -> str:
    title = (
        "## Apresentação do Sumário Executivo"
        if data["language"] == "Portuguese"
        else "## Executive Summary Presentation"
    )
    payload = {"language": data["language"], "project_description": description}
    body = llm.call(prompts.EXEC_SUMMARY_PRESENTATION, json.dumps(payload), temperature=0.3)
    return title + "\n\n" + body
