from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import validator
from proposal_builder.helpers import read_prompt
from pathlib import Path


class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: Optional[str] = ''
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_DEPLOYMENT: str
    OPENAI_API_KEY: str
    OPENAI_API_VERSION: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str
    API_URL: str

    class Config:
        env_file = ".env"


DIR = Path(__file__).parent
PROMPTS_PATH = DIR / "proposal_builder" / "prompts"

class Prompts:
    SYSTEM_PROMPT = read_prompt( PROMPTS_PATH / "system_prompt.txt")
    PROJECT_DESCRIPTION = read_prompt( PROMPTS_PATH / "project_description.txt") 
    EXECUTIVE_SUMMARY = read_prompt( PROMPTS_PATH / "executive_summary.txt") 
    TIMELINE_AND_PLANING_GENOS = read_prompt( PROMPTS_PATH / "timeline_and_planing_GENOS.txt") 
    TIMELINE_AND_PLANING_COCREATION = read_prompt( PROMPTS_PATH / "timeline_and_planing_CoCreation.txt") 
    TIMELINE_AND_PLANING_CLOSED_PROJECT = read_prompt( PROMPTS_PATH / "timeline_and_planing_ClosedProject.txt") 
    STAKEHOLDERS_AND_TEAM = read_prompt( PROMPTS_PATH / "stakeholders_and_team.txt")
    REQUIREMENTS_AND_PRICING = read_prompt( PROMPTS_PATH / "requirements_and_pricing.txt")     
    GENOS = read_prompt( PROMPTS_PATH / "gen_os.txt")     
    AGENTS_ARCHETYPES = read_prompt( PROMPTS_PATH / "agentic_archetypes.txt")     

settings = Settings()
prompts = Prompts()