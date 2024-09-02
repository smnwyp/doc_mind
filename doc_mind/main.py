import streamlit as st

from component.sidebar import sidebar
from helper.ui import is_query_valid

st.set_page_config(page_title="DocMind", page_icon="📖", layout="wide")
st.header("📖DocMind")

sidebar()

MODEL_LIST = ["space-phi-3.5"]
model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Upload your document here!",
)

if not uploaded_file:
    st.stop()


st.text_area(label="Initial analysis from DocMind:", value="magic mind reader!")

with st.form(key="qa_form"):
    query = st.text_area("Ask your question on the document")
    submit = st.form_submit_button("Submit")

if submit:
    if not is_query_valid(query):
        st.stop()

    # Output Columns
    answer_col, sources_col = st.columns(2)

    result = {"answer": "sth sensible.",
              "sources": [{"page_content": "real content1",
                           "meta_source": "p1"},
                          {"page_content": "real content2",
                           "meta_source": "p2"}
                          ]}

    with answer_col:
        st.markdown("#### Answer")
        st.markdown("sth sensible here.")

    with sources_col:
        st.markdown("#### Sources")
        for source in result["sources"]:
            st.markdown(source["page_content"])
            st.markdown(source["meta_source"])
            st.markdown("---")
