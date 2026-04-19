import json
import os
from pathlib import Path

import streamlit as st

from proposal_builder.helpers import read_prompt


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def _get_setting(key: str, default: str | None = None) -> str | None:
    """Priority: Streamlit secrets → environment variable → default."""
    try:
        return st.secrets[key]
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv(key, default)


class Settings:
    AZURE_OPENAI_API_KEY = _get_setting("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT = _get_setting("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_VERSION = _get_setting("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_DEPLOYMENT = _get_setting("AZURE_OPENAI_DEPLOYMENT")
    OPENAI_API_KEY = _get_setting("OPENAI_API_KEY")
    OPENAI_API_VERSION = _get_setting("OPENAI_API_VERSION")
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = _get_setting("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

    def validate(self) -> None:
        required = (
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT",
        )
        missing = [k for k in required if not getattr(self, k)]
        if missing:
            raise EnvironmentError(
                f"Missing required Azure OpenAI configuration: {', '.join(missing)}. "
                "Set these in your .env file or Streamlit secrets."
            )


# ---------------------------------------------------------------------------
# Prompts — auto-discovered from proposal_builder/prompts/*.txt
# Attribute name = filename stem in UPPER_CASE  (e.g. system_prompt.txt → SYSTEM_PROMPT)
# ---------------------------------------------------------------------------

class Prompts:
    def __init__(self, prompts_path: Path) -> None:
        for path in sorted(prompts_path.glob("*.txt")):
            setattr(self, path.stem.upper(), read_prompt(path))

    def __getattr__(self, name: str):
        available = [k for k in self.__dict__ if not k.startswith("_")]
        raise AttributeError(
            f"Prompt '{name}' not found. "
            f"Drop a .txt file in prompts/ with the matching stem. "
            f"Available: {available}"
        )


# ---------------------------------------------------------------------------
# Templates — auto-discovered from proposal_builder/templates/*
# .md / .txt files are loaded as strings; .json files are parsed as dicts.
# Attribute name = filename stem in UPPER_CASE  (e.g. work_agreement_en.md → WORK_AGREEMENT_EN)
# ---------------------------------------------------------------------------

class Templates:
    def __init__(self, templates_path: Path) -> None:
        for path in sorted(templates_path.glob("*")):
            if path.suffix == ".json":
                with open(path, encoding="utf-8") as f:
                    setattr(self, path.stem.upper(), json.load(f))
            elif path.suffix in (".md", ".txt"):
                setattr(self, path.stem.upper(), path.read_text(encoding="utf-8"))

    def __getattr__(self, name: str):
        available = [k for k in self.__dict__ if not k.startswith("_")]
        raise AttributeError(
            f"Template '{name}' not found. "
            f"Drop a file in templates/ with the matching stem. "
            f"Available: {available}"
        )


# ---------------------------------------------------------------------------
# Singletons
# ---------------------------------------------------------------------------

_DIR = Path(__file__).parent

settings = Settings()
prompts = Prompts(_DIR / "proposal_builder" / "prompts")
templates = Templates(_DIR / "proposal_builder" / "templates")
