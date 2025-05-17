"""
Main application entry point for the Proposal Builder.
Handles the Streamlit UI and integrates with the async API.
"""

import json
import time
import requests
import streamlit as st
from src.streamlit_helpers import (
    setup_page_config,
    apply_styles,
    render_proposal_form,
    render_footer
)

# API configuration
API_URL = "http://api:8000"  # Docker service name

def main():
    """Main application function"""
    # Configure the page
    setup_page_config()
    
    # Apply custom styling
    apply_styles()
    
    # Render header
    st.markdown('<div class="header-container"><h1 style="text-align: center;">DareData Proposal Builder</h1></div>', unsafe_allow_html=True)
    
    # Get proposal data from form
    proposal_data, submitted = render_proposal_form()
    
    # Display results if form was submitted
    if submitted:
        with st.spinner("Generating proposal..."):
            # Submit to async API
            try:
                response = requests.post(f"{API_URL}/proposals/", json=proposal_data)
                response.raise_for_status()
                proposal_info = response.json()
                
                # Store the proposal ID in session state
                st.session_state["proposal_id"] = proposal_info["proposal_id"]
                st.session_state["proposal_submitted"] = True
                
                # Inform user
                st.success("Proposal submitted for processing!")
            except Exception as e:
                st.error(f"Error submitting proposal: {str(e)}")
    
    # Check for and display completed proposal
    if st.session_state.get("proposal_submitted", False):
        proposal_id = st.session_state["proposal_id"]
        
        # Poll for status
        try:
            response = requests.get(f"{API_URL}/proposals/{proposal_id}")
            response.raise_for_status()
            proposal_info = response.json()
            
            # Display status
            status = proposal_info["status"]
            if status == "processing":
                st.info("Proposal is still being processed...")
                # Auto-refresh
                time.sleep(1)
                st.rerun()
            elif status == "completed":
                # Display the results in tabs
                st.success("Proposal generated successfully!")
                display_results(proposal_info)
                
                # Option to start a new proposal
                if st.button("Create New Proposal"):
                    # Clear session state
                    st.session_state.pop("proposal_submitted", None)
                    st.session_state.pop("proposal_id", None)
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Error checking proposal status: {str(e)}")
    
    # Render footer
    render_footer()

def display_results(proposal_info):
    """
    Display the results of the proposal generation.
    
    Args:
        proposal_info: Information about the generated proposal
    """
    # Get markdown and JSON
    markdown_content = proposal_info.get("markdown", "")

    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.markdown(markdown_content)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    # Initialize session state
    if "proposal_submitted" not in st.session_state:
        st.session_state["proposal_submitted"] = False
    
    main()