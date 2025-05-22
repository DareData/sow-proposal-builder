"""
Core functionality for the Proposal Builder application.
"""

import streamlit as st
import datetime
from typing import Dict, Tuple, Any


def setup_page_config() -> None:
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="DareData Proposal Builder",
        page_icon="📝",
        layout="centered",
        initial_sidebar_state="collapsed"
    )


def apply_styles() -> None:
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
        /* Main color scheme */
        :root {
            --primary-color: #6a0dad;
            --secondary-color: #8a2be2;
            --text-color: #333333;
            --bg-color: #ffffff;
            --accent-color: #e6e6fa;
        }
        
        /* Header styling */
        .header-container {
            background-color: var(--primary-color);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Form styling */
        .form-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Section headers */
        .section-header {
            color: var(--primary-color);
            font-weight: bold;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 0.5rem;
        }
        
        /* Button styling */
        div.stButton > button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        
        div.stButton > button:hover {
            background-color: var(--secondary-color);
        }
        
        /* Result container */
        .result-container {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 2rem;
            border: 1px solid #e0e0e0;
        }
        
        /* Copy button */
        .copy-button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            cursor: pointer;
        }
        
        .copy-button:hover {
            background-color: var(--secondary-color);
        }
        
        /* Adjust text area height */
        .stTextArea textarea {
            min-height: 100px;
        }
        
        /* Field labels */
        label {
            font-weight: bold;
            color: var(--text-color);
        }
        
        /* Header text */
        h1, h2, h3 {
            color: var(--primary-color);
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #666;
            font-size: 0.8rem;
        }
        
        /* Status indicators */
        .status-processing {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 5px;
            padding: 0.5rem;
            color: #856404;
        }
        
        .status-completed {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 0.5rem;
            color: #155724;
        }
        
        .status-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 0.5rem;
            color: #721c24;
        }
    </style>
    """, unsafe_allow_html=True)


def render_proposal_form() -> Tuple[Dict[str, Any], bool]:
    """
    Render the proposal form and collect input data.
    
    Returns:
        Tuple containing:
            - Dictionary with proposal data
            - Boolean indicating if form was submitted
    """
    proposal_data = {}
    
    with st.form("proposal_form"):
        st.markdown('<h2 class="section-header">Client Information</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("**Client Name**", key="client_name")
        
        with col2:
            scope = st.selectbox(
                "**National / International**",
                options=["National", "International"],
                key="scope"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox(
                "**Proposal Language**",
                options=["Portuguese", "English"],
                key="language"
            )
        
        with col2:
            project_name = st.text_input("**Project Name**", key="project_name")
        
        project_type = st.selectbox(
            "**Project Type**",
            options=["Co-Creation", "Gen-OS", "Closed Project"],
            key="project_type"
        )
        
        st.markdown('<h2 class="section-header">Project Details</h2>', unsafe_allow_html=True)
        
        main_goals = st.text_area("**Main Goals and Deliverables**", key="main_goals")
        
        technology_focus = st.selectbox(
            "**Technology Focus**",
            options=["AWS", "GCP", "Azure", "OnPrem"],
            key="technology_focus"
        )
        
        general_description = st.text_area("**General Description**", key="general_description")
        
        st.markdown('<h2 class="section-header">Planning and Team</h2>', unsafe_allow_html=True)
        
        planning = st.text_area("**Planning - Timeline, Team Effort and Project Milestones**", key="planning")
        
        col1, col2 = st.columns(2)
        with col1:
            client_stakeholders = st.text_area("**Key Client Stakeholders**", key="client_stakeholders")
        
        with col2:
            daredata_team = st.text_area("**DareData Team**", key="daredata_team")
        
        st.markdown('<h2 class="section-header">Additional Information</h2>', unsafe_allow_html=True)
        
        client_expectations = st.text_area("**What we expect from Client**", key="client_expectations")
        
        special_conditions = st.text_area("**Special Financial Conditions**", key="special_conditions")

        col1, col2 = st.columns(2)
        with col1:
            mlops_guidelines = st.selectbox(
                "**MLOps Guidelines**",
                options=["Yes", "No"],
                key="mlops_guidelines"
            )
        with col2:
            agentic_archetypes_guidelines = st.selectbox(
                "**Agentic Archetype Guidelines**",
                options=["Yes", "No"],
                key="agentic_archetypes_guidelines"
            )
        
        submitted = st.form_submit_button("Generate Proposal")
    
    if submitted:
        # Create proposal data as JSON
        proposal_data = {
            "client_name": client_name,
            "scope": scope,
            "language": language,
            "project_name": project_name,
            "project_type": project_type,
            "main_goals": main_goals,
            "technology_focus": technology_focus,
            "general_description": general_description,
            "planning": planning,
            "client_stakeholders": client_stakeholders,
            "daredata_team": daredata_team,
            "client_expectations": client_expectations,
            "special_conditions": special_conditions,
            "mlops_guidelines": mlops_guidelines,
            "agentic_archetypes_guidelines": agentic_archetypes_guidelines,
        }
    
    return proposal_data, submitted


def render_footer() -> None:
    """Render the application footer."""
    st.markdown("""
        <style>
            .footer {
                text-align: center;
                margin-top: 3rem;
                color: #666;
                font-size: 0.8rem;
            }
        </style>
        <div class="footer">
            © DareData 2025 | Proposal Builder v1.0
        </div>
    """, unsafe_allow_html=True)
