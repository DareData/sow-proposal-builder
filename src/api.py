"""
FastAPI backend for handling asynchronous proposal generation.
"""

import json
import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.proposal_builder.agent import agenerate_proposal

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
    scope: str
    language: str
    project_name: str
    project_type: str
    main_goals: str
    technology_focus: str
    general_description: str
    planning: str
    client_stakeholders: str
    daredata_team: str
    client_expectations: str
    special_conditions: str

class ProposalResponse(BaseModel):
    proposal_id: str
    status: str
    created_at: str
    completed_at: Optional[str] = None
    markdown: Optional[str] = None

async def generate_proposal_async(proposal_id: str, proposal_data: Dict[str, Any]):
    """
    Asynchronous function to generate proposal.
    In real-world scenarios, this could be a complex, time-consuming task.
    
    Args:
        proposal_id: Unique identifier for the proposal
        proposal_data: Dictionary with proposal information
    """
    # Simulate processing time for demonstration
    import asyncio
    await asyncio.sleep(2)
    
    # Generate markdown and update the proposal status
    markdown = await agenerate_proposal(proposal_data)
    
    # Update the stored proposal
    proposals_db[proposal_id]["status"] = "completed"
    proposals_db[proposal_id]["completed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    proposals_db[proposal_id]["markdown"] = markdown



@app.post("/proposals/", response_model=ProposalResponse)
async def create_proposal(proposal: ProposalRequest, background_tasks: BackgroundTasks):
    """
    Submit a new proposal for asynchronous generation.
    
    Args:
        proposal: Proposal data
        background_tasks: FastAPI background tasks handler
        
    Returns:
        Basic proposal information with ID for status checking
    """
    # Create a unique proposal ID
    import uuid
    proposal_id = str(uuid.uuid4())
    
    # Current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create proposal data dictionary
    proposal_data = proposal.dict()
    proposal_data["created_at"] = timestamp
    
    # Store proposal with initial status
    proposals_db[proposal_id] = {
        "proposal_id": proposal_id,
        "status": "processing",
        "created_at": timestamp,
        "completed_at": None,
        "markdown": None,
    }
    
    # Schedule the async processing task
    background_tasks.add_task(generate_proposal_async, proposal_id, proposal_data)
    
    # Return immediately with the proposal ID for status checking
    return ProposalResponse(
        proposal_id=proposal_id,
        status="processing",
        created_at=timestamp
    )

@app.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(proposal_id: str):
    """
    Get proposal by ID.
    
    Args:
        proposal_id: Unique proposal identifier
        
    Returns:
        Proposal data with status and markdown if complete
    """
    if proposal_id not in proposals_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return proposals_db[proposal_id]

@app.get("/proposals/", response_model=Dict[str, ProposalResponse])
async def list_proposals():
    """
    List all proposals.
    
    Returns:
        Dictionary of all proposals
    """
    return proposals_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)