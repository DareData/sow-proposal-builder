"""
Main application entry point for the Proposal Builder.
Handles the Streamlit UI and integrates with the simplified API.
"""
import streamlit as st
from streamlit_helpers import (
    setup_page_config,
    apply_styles,
    render_proposal_form,
    render_footer
)
from proposal_builder.agent import generate_proposal

def main():
    """Main application function"""
    # Configure the page
    setup_page_config()
   
    # Apply custom styling
    apply_styles()
   
    # Render header
    st.markdown('<div class="header-container"><h1 style="text-align: center;">DareData Proposal Builder</h1></div>', unsafe_allow_html=True)
   
    # Initialize session state
    if "proposal_generated" not in st.session_state:
        st.session_state["proposal_generated"] = False
    if "proposal_markdown" not in st.session_state:
        st.session_state["proposal_markdown"] = ""
    if "last_proposal_data" not in st.session_state:
        st.session_state["last_proposal_data"] = {}
    
    # Always show the form (whether or not a proposal has been generated)
    proposal_data, submitted = render_proposal_form()
    
    # Handle form submission
    if submitted:
        generate_and_display_proposal(proposal_data)
    
    # Show proposal results if available
    if st.session_state["proposal_generated"] and st.session_state["proposal_markdown"]:
        st.markdown("---")  # Add a divider between form and results
        display_results(st.session_state["proposal_markdown"])
        
        # Option to clear results and start fresh
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Clear Results", type="secondary"):
                st.session_state["proposal_generated"] = False
                st.session_state["proposal_markdown"] = ""
                st.rerun()
   
    # Render footer
    render_footer()

def generate_and_display_proposal(proposal_data):
    """
    Submit proposal to the API and display results
   
    Args:
        proposal_data: Dictionary containing proposal form data
    """
    with st.spinner("Generating proposal... This may take a moment."):
        try:
            # Submit to API
            #response = requests.post(f"{API_URL}/proposals/", json=proposal_data)
            #response.raise_for_status()
            #proposal_info = response.json()
           
            # Store the markdown and proposal data
            #markdown_content = proposal_info.get("markdown", "")
            markdown_content = generate_proposal(proposal_data)
            st.session_state["proposal_markdown"] = markdown_content
            st.session_state["last_proposal_data"] = proposal_data
            st.session_state["proposal_generated"] = True
           
            # Force a rerun to display the proposal
            st.rerun()
        except Exception as e:
            st.error(f"Error generating proposal: {str(e)}")

def display_results(markdown_content):
    """
    Display the generated proposal.
   
    Args:
        markdown_content: The markdown content of the proposal
    """
    # Display success message
    st.success("Proposal generated successfully! You can modify the form above and regenerate if needed.")
   
    # Display in a container with styling
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.markdown(markdown_content)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()