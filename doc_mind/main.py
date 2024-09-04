import time

import streamlit as st

from component.sidebar import sidebar
from helper.ui import is_query_valid

st.set_page_config(page_title="DocMind", page_icon="📖", layout="wide")
st.header("DocMind 🧠")

sidebar()

MODEL_LIST = ["docmind-model"]
model: str = st.selectbox("DocMind Model", options=MODEL_LIST)  # type: ignore

uploaded_file = st.file_uploader(
    "📈 Upload a pdf or an image file",
    type=["pdf", "jpg"],
    help="Upload your document here!",
)

if not uploaded_file:
    st.stop()

with st.spinner("⏳ DocMind is reading the document, this may take a while"):
    time.sleep(2)

dummy_reader = "magic mind reader! \n" + "magic analysis 1 \n" + "magic analysis 2 \n"
st.text_area(label="💫 Initial analysis from DocMind:", value=dummy_reader)

with st.form(key="qa_form"):
    query = st.text_area("😌 Any further questions you'd like to ask about the document?")
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
