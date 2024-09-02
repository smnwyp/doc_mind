import streamlit as st

from component.faq import faq

def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Upload a pdf, docx, or txt file \n"
            "2. Review DocMind's take on the file \n"
            "3. Ask a question about the document \n"
        )

        st.session_state["OPENAI_API_KEY"] = ""

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "DocMind is a document mind reader."
        )
        st.markdown("---")

        faq()