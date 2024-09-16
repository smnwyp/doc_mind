import streamlit as st

from component.faq import faq
from helper.core import make_api_call, get_session_id


# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False

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
        uploaded_file = st.file_uploader(
            "📈 Upload a pdf or an image file",
            type=["pdf", "jpg"],
            help="Upload your document here!",
        )

        if not uploaded_file:
            st.stop()

        with st.spinner("⏳ DocMind is reading the document, this may take a while"):
            session_id = get_session_id()
            print(f"sidebar {session_id=}")
            upload_doc = make_api_call(prompt="summarize the content", file=uploaded_file,
                                             session_id=get_session_id(creat_new=True))
            if upload_doc:
                st.success("DocMind has successfully performed initial analysis on the document you uploaded🛸. \n"
                           " See a short summary in the main chat. ➡️")
                print(f"'file_processed' in st.session_state = {'file_processed' in st.session_state}")
                st.session_state.file_processed = True
                print(f"sidebar == {st.session_state.file_processed=}")
                # summary = summarize_result["response"]
                # st.text_area(label="💫 Initial analysis from DocMind:", value=summary)
