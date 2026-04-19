# SOW Proposal Builder

Streamlit web app that generates Statement of Work proposals for DareData's consulting engagements using Azure OpenAI (GPT-4o). Proposals are produced in English or Portuguese (PT-PT) and follow a fixed multi-section structure.

## Architecture

```
src/
├── app.py                        # Streamlit entry point — session state, layout
├── api.py                        # FastAPI wrapper (defined but not called by frontend)
├── config.py                     # Settings, Prompts, Templates singletons (auto-discovered)
├── streamlit_helpers.py          # All Streamlit UI widgets and form rendering
└── proposal_builder/
    ├── agent.py                  # Thin orchestrator — phases 1-3, no inline prose
    ├── llm_caller.py             # LLMCaller class + get_llm() lazy singleton
    ├── frameworks.py             # FRAMEWORK_REGISTRY + append_frameworks()
    ├── static_sections.py        # get_pricing(), get_sifide(), get_work_agreement()
    ├── llm.py                    # AzureOpenAI client factory
    ├── helpers.py                # read_prompt(), strip_code_fence()
    ├── prompts/                  # LLM instruction files (*.txt), auto-discovered by config.py
    │   ├── system_prompt.txt
    │   ├── project_description.txt
    │   ├── executive_summary.txt
    │   ├── exec_summary_presentation.txt
    │   ├── timeline_and_planning.txt
    │   ├── daredata_team.txt
    │   ├── requirements_and_pricing.txt
    │   ├── gen_os.txt
    │   ├── gen_os_pt.txt
    │   ├── mlops.txt
    │   ├── devops.txt
    │   ├── llmops.txt
    │   └── wow.txt
    └── templates/                # Static output content (*.md / *.json), auto-discovered
        ├── pricing_gen_os_en.md
        ├── pricing_gen_os_pt.md
        ├── pricing_standard_en.md
        ├── pricing_standard_pt.md
        ├── sifide_pt.md
        ├── work_agreement_en.md
        ├── work_agreement_pt.md
        ├── payment_terms_en.json
        └── payment_terms_pt.json
```

## Proposal generation flow

`render_proposal_form()` → `proposal_data` dict → `generate_proposal(data)` → Markdown string.

`generate_proposal()` runs in three explicit phases:

**Phase 1 — LLM sections** (computed in dependency order):
1. `_project_description` — builds prompt, appends enabled frameworks via `append_frameworks()`, optional Gen-OS second pass
2. `_timeline_planning`
3. `_daredata_team`
4. `_requirements` — skipped entirely (no LLM call) when `client_expectations` is empty
5. `_executive_summary` — must run after `_project_description` (uses its output)
6. `_exec_summary_presentation` — also depends on `_project_description`

**Phase 2 — Static sections** (no LLM, loaded from `templates/`):
- `get_pricing(project_type, language)`
- `get_sifide()` — Portuguese only
- `get_work_agreement(project_type, language, special_conditions)`

**Phase 3 — Assembly** (document/reader order, empty sections auto-filtered):
```
exec_summary → project_desc → timeline → team → requirements →
pricing → sifide → work_agreement → exec_presentation
```

Every LLM call goes through a single abstraction in `llm_caller.py`:
```python
llm.call(system_prompt, user_content, temperature=0.7, extra_messages=None)
```

The client is created lazily on first call via `get_llm()`. Missing credentials raise a clear `EnvironmentError` shown as a Streamlit error box rather than a traceback.

## The `proposal_data` dict schema

All keys passed from `render_proposal_form()`:

```python
{
    "client_name":          str,
    "language":             "Portuguese" | "English",
    "project_name":         str,
    "project_type":         "Co-Creation" | "Gen-OS" | "Closed Project",
    "technology_focus":     "AWS" | "GCP" | "Azure" | "OnPrem",
    "general_description":  str,
    "extended_description": bool,   # True → second LLM pass for longer description
    "planning":             str,
    "daredata_team":        str,
    "client_expectations":  str,    # empty → _requirements() is skipped
    "special_conditions":   str,    # non-empty → appended to work agreement
    "mlops":                "Yes" | "No",
    "devops":               "Yes" | "No",
    "llmops":               "Yes" | "No",
    "wow":                  "Yes" | "No",   # Ways of Working
}
```

## Editing prompts and templates

**Prompts** (`src/proposal_builder/prompts/*.txt`) are LLM instructions — they shape how the model writes each section. Drop a new `.txt` file and it is immediately available as `prompts.FILENAME_STEM` (uppercase). No code change needed.

**Templates** (`src/proposal_builder/templates/`) are static output — final prose that appears verbatim in the proposal without an LLM call. `.md` files load as strings; `.json` files load as dicts. Drop a new file and it is available as `templates.FILENAME_STEM` (uppercase).

Both directories are scanned at startup. Restart the Streamlit server after any file change.

## Key constraints

- `PYTHONPATH` must include `src/` — the code uses bare imports like `from config import settings`.
- The FastAPI backend (`api.py`) is defined but the Streamlit frontend calls `generate_proposal()` directly. The backend is intended for future API-first usage.
- No automated test suite exists. Use `tests.ipynb` for manual end-to-end testing.
