import streamlit as st

from helper.core import call_sumarize

def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Upload a pdf, docx, or txt file \n"
            "2. Review DocMind's take on the file \n"
            "3. Ask a question about the document \n"
        )


        # st.markdown("---")
        # faq()

        st.markdown("---")

        if not st.session_state.file_processed:
            uploaded_file = st.sidebar.file_uploader(
                "📈 Upload a pdf or an image file",
                type=["pdf", "jpg"],
                help="Upload your document here!",
            )

            if not uploaded_file:
                st.stop()

            with st.spinner("⏳ DocMind is reading the document, this may take a while"):
                initial_analysis = call_sumarize(file=uploaded_file)
                if initial_analysis:
                    st.sidebar.success(
                        "DocMind has successfully performed initial analysis on the document you uploaded🛸. \n"
                        " See a short summary in the main chat. ➡️")
                    st.session_state.file_processed = True
                    print(f"sidebar == {st.session_state.file_processed=}")
                    st.session_state.context = initial_analysis["context"]
                    st.session_state.summary = initial_analysis["response"]