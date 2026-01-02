import os
import streamlit as st

from proposal_builder.helpers import read_prompt
from pathlib import Path

def get_setting(key: str, default: str = None):
    """
    Get a setting from Streamlit secrets, environment variables, or default value
    Priority: Streamlit secrets > Environment variables > Default
    """
    try:
        # Try Streamlit secrets first (production)
        return st.secrets[key]
    except:
        # Fall back to environment variables (local development)
        from dotenv import load_dotenv
        load_dotenv()
        
        return os.getenv(key, default)

# Simple settings class (optional - keeps your existing usage pattern)
class Settings:
    AZURE_OPENAI_API_KEY = get_setting("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT = get_setting("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_VERSION = get_setting("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_DEPLOYMENT = get_setting("AZURE_OPENAI_DEPLOYMENT")
    OPENAI_API_KEY = get_setting("OPENAI_API_KEY")
    OPENAI_API_VERSION = get_setting("OPENAI_API_VERSION")
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = get_setting("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

DIR = Path(__file__).parent
PROMPTS_PATH = DIR / "proposal_builder" / "prompts"

class Prompts:
    SYSTEM_PROMPT = read_prompt( PROMPTS_PATH / "system_prompt.txt")
    PROJECT_DESCRIPTION = read_prompt( PROMPTS_PATH / "project_description.txt") 
    EXECUTIVE_SUMMARY = read_prompt( PROMPTS_PATH / "executive_summary.txt") 
    TIMELINE_AND_PLANNING_GENOS = read_prompt( PROMPTS_PATH / "timeline_and_planning_GENOS.txt") 
    TIMELINE_AND_PLANNING_COCREATION = read_prompt( PROMPTS_PATH / "timeline_and_planning_CoCreation.txt") 
    TIMELINE_AND_PLANNING_CLOSED_PROJECT = read_prompt( PROMPTS_PATH / "timeline_and_planning_ClosedProject.txt") 
    STAKEHOLDERS_AND_TEAM = read_prompt( PROMPTS_PATH / "stakeholders_and_team.txt")
    REQUIREMENTS_AND_PRICING = read_prompt( PROMPTS_PATH / "requirements_and_pricing.txt")     
    GENOS = read_prompt( PROMPTS_PATH / "gen_os.txt")       
    MLOPS = read_prompt( PROMPTS_PATH / "mlops.txt")
    DEV_OPS = read_prompt( PROMPTS_PATH / "devops.txt")

settings = Settings()
prompts = Prompts()