"""
FastAPI backend for handling asynchronous proposal generation.
"""

from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from proposal_builder.agent import generate_proposal

app = FastAPI(title="Proposal Builder API", description="Async API for proposal generation")

# Add CORS middleware to allow Streamlit to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for proposals - would use a DB in production
proposals_db = {}

class ProposalRequest(BaseModel):
    client_name: str
    language: str
    project_name: str
    project_type: str
    technology_focus: str
    general_description: str
    planning: str
    client_stakeholders: str
    daredata_team: str
    client_expectations: str
    special_conditions: str

class ProposalResponse(BaseModel):
    markdown: Optional[str] = None


@app.post("/proposals/", response_model=ProposalResponse)
async def create_proposal(proposal: ProposalRequest):
    # Create proposal data dictionary
    proposal_data = proposal.model_dump()
    markdown = generate_proposal(proposal_data)
    
    return ProposalResponse(
        markdown=markdown,
    )


@app.get("/health")
async def health_check():
    return {"status: ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)