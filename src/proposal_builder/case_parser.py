"""
Parser for Project_Storytelling.md.

Splits the markdown by heading level:
  # = client/company
  ## = project (one case per project)
  ### = subproject (folded into parent project)
  #### or **Bold** = section within a project

Each case is a dict with: client, project, and section fields
(summary, vertical_details, business_storytelling, technical_storytelling,
technologies, success_metrics, sales_context).

Cases where the summary is empty or "TBD" are excluded.
"""
from __future__ import annotations

import re
from pathlib import Path

_SECTION_ALIASES = {
    "summary": "summary",
    "vertical details": "vertical_details",
    "vertical_details": "vertical_details",
    "business storytelling": "business_storytelling",
    "business_storytelling": "business_storytelling",
    "technical storytelling": "technical_storytelling",
    "technical_storytelling": "technical_storytelling",
    "technologies": "technologies",
    "success metrics": "success_metrics",
    "success_metrics": "success_metrics",
    "sales context": "sales_context",
    "sales_context": "sales_context",
}

_HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)(?:\s*\{#[^}]*\})?\s*$")
_BOLD_LABEL_RE = re.compile(r"^\*\*([^*]+)\*\*\s*$")


def _normalise_section(name: str) -> str | None:
    return _SECTION_ALIASES.get(name.strip().lower())


def _is_tbd(text: str) -> bool:
    cleaned = text.strip().lower()
    return cleaned in ("", "tbd", "* tbd")


def parse_cases(md_path: str | Path) -> list[dict]:
    text = Path(md_path).read_text(encoding="utf-8")
    lines = text.splitlines()

    cases: list[dict] = []
    current_client: str = ""
    current_project: str = ""
    current_sections: dict[str, list[str]] = {}
    current_section_key: str | None = None

    def _flush():
        nonlocal current_project, current_sections, current_section_key
        if not current_project or not current_sections:
            return
        sections = {k: "\n".join(v).strip() for k, v in current_sections.items()}
        if _is_tbd(sections.get("summary", "")):
            return
        cases.append({
            "client": current_client,
            "project": current_project,
            **sections,
        })

    for line in lines:
        heading_match = _HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # strip trailing status markers like (*tbd*), (TBD), (*tbu*), (*tbc*)
            title = re.sub(r"\s*\(\*?(?:tbd|tbu|tbc)\*?\)\s*$", "", title, flags=re.IGNORECASE)

            if level == 1:
                _flush()
                current_client = title
                current_project = ""
                current_sections = {}
                current_section_key = None
            elif level == 2:
                _flush()
                current_project = title
                current_sections = {}
                current_section_key = None
            elif level == 3:
                # subproject — fold content into parent project
                current_section_key = None
            elif level == 4:
                sec = _normalise_section(title)
                if sec:
                    current_section_key = sec
                    current_sections.setdefault(sec, [])
                else:
                    current_section_key = None
            continue

        bold_match = _BOLD_LABEL_RE.match(line)
        if bold_match:
            sec = _normalise_section(bold_match.group(1))
            if sec:
                current_section_key = sec
                current_sections.setdefault(sec, [])
                continue

        if current_section_key and current_project:
            current_sections.setdefault(current_section_key, []).append(line)

    _flush()
    return [c for c in cases if c["project"] != "Project Name"]


def build_compact_catalog(cases: list[dict]) -> str:
    """One-paragraph summary per case for LLM selection."""
    parts = []
    for i, case in enumerate(cases):
        summary = case.get("summary", "")
        techs = case.get("technologies", "")
        metrics = case.get("success_metrics", "")
        block = f"[CASE {i}] {case['project']}\n"
        if summary:
            block += f"Summary: {summary[:500]}\n"
        if techs:
            block += f"Technologies: {techs[:300]}\n"
        if metrics:
            block += f"Metrics: {metrics[:300]}\n"
        parts.append(block)
    return "\n---\n".join(parts)
