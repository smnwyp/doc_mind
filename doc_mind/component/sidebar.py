import streamlit as st
import streamlit.components.v1 as components
from streamlit_modal import Modal

from helper.display import user, assistant
from helper.typings import Message
from helper.core import call_sumarize, send_feedback

def sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color:  #e6f3f3;
    }
    .stMarkdown {
        color: #003333;
    }
     h1, h2, h3 {
         color: #003333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(
            "💸💸 It's totally FREE to use Docmind !!\n"
            "🤞🏻🤞🏻 Docmind does NOT store your data \n"
            "# How to use\n"            
            "1. Upload a pdf or image file in the sidebar \n"
            "2. Review DocMind's initial analysis in the main chat \n"
            "3. Ask Docmind follow-up questions and be amazed 👍🏻 \n"
        )

        # Main Streamlit app

        # Replace this with your YouTube video URL
        video_url = "https://www.youtube.com/embed/hFk0VKcM1ns?si=6OfHmpouGIjysUdJ"

        if 'show_modal' not in st.session_state:
            st.session_state.show_modal = False

            # Button to trigger modal
        if st.button("Click to Watch How to Use Docmind"):
            st.session_state.show_modal = True

            # Create modal
        modal = Modal(key="video_modal", title="How to use Docmind")

        if st.session_state.show_modal:
            with modal.container():
                st.components.v1.iframe(video_url, width=640, height=360)

                # Button to close modal
                if st.button("Close Video"):
                    st.session_state.show_modal = False

            # Check if modal is closed (including by the "x" button)
            if not modal.is_open():
                st.session_state.show_modal = False

        # st.markdown("---")
        # faq()
        st.markdown(
            "Interested in customized solutions? Contact us at contact.docmind@gmail.com .")

        st.markdown("---")
        st.markdown(
            "# Upload File Here\n")

        if not st.session_state.file_processed:
            uploaded_file = st.sidebar.file_uploader(
                "",
                type=["pdf", "jpg"],
                help="Upload your document here!",
            )

            if not uploaded_file:
                st.stop()

            with st.spinner("⏳ DocMind is reading the document, this may take a while"):
                initial_analysis = call_sumarize(file=uploaded_file)
                if initial_analysis:
                    st.sidebar.success(
                        "See the initial analysis 🛸 provided by DocMind in the main chat 👉🏻 ")
                    st.session_state.file_processed = True
                    print(f"sidebar == {st.session_state.file_processed=}")
                    st.session_state.context = initial_analysis["context"]
                    st.session_state.summary = initial_analysis["response"]

        display_sidebar_feedback()


def display_sidebar_feedback():
    st.sidebar.header("Feedback")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("👍 Like"):
            send_feedback(feedback_type="like", unique_id=st.session_state.context)
            st.success("😁")

    with col2:
        if st.button("👎 Dislike"):
            send_feedback(feedback_type="dislike", unique_id=st.session_state.context)
            st.error("🥹")

