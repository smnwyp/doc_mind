import streamlit as st
import streamlit.components.v1 as components
from streamlit_modal import Modal

from helper.core import call_sumarize


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Upload a pdf, docx, or txt file \n"
            "2. Review DocMind's take on the file \n"
            "3. Ask a question about the document \n"
        )

        # Main Streamlit app
        st.title("Video Pop-up Example")

        # Replace this with your YouTube video URL
        video_url = "https://www.youtube.com/embed/hFk0VKcM1ns?si=6OfHmpouGIjysUdJ"

        if 'show_modal' not in st.session_state:
            st.session_state.show_modal = False

            # Button to trigger modal
        if st.button("Show Video"):
            st.session_state.show_modal = True

            # Create modal
        modal = Modal(key="video_modal", title="How to use Docmind")

        if st.session_state.show_modal:
            with modal.container():
                st.components.v1.iframe(video_url, width=640, height=360)

                # Button to close modal
                if st.button("Close Video"):
                    st.session_state.show_modal = False
                    st.experimental_rerun()

            # Check if modal is closed (including by the "x" button)
            if not modal.is_open():
                st.session_state.show_modal = False
                st.experimental_rerun()

        st.write("Click the button above to see the video pop-up!")

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
            st.success("Thank you for your feedback!")

    with col2:
        if st.button("👎 Dislike"):
            st.error("We're sorry to hear that. We'll try to improve!")

