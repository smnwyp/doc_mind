import streamlit as st

from helper.core import make_api_call, send_request, dummy_call_summarize, dummy_call_chat
import streamlit as st

from helper.core import make_api_call, get_session_id


st.set_page_config(page_title="DocMind", page_icon="📖", layout="wide")
st.header("DocMind 🧠")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False

initial_analysis = None

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
        initial_analysis = dummy_call_summarize(doc=uploaded_file)
        # upload_doc = make_api_call(prompt="summarize the content", file=uploaded_file,
        #                                  session_id=get_session_id(creat_new=True))
        if initial_analysis:
            st.success("DocMind has successfully performed initial analysis on the document you uploaded🛸. \n"
                       " See a short summary in the main chat. ➡️")
            # print(f"'file_processed' in st.session_state = {'file_processed' in st.session_state}")
            st.session_state.file_processed = True
            print(f"sidebar == {st.session_state.file_processed=}")
            # summary = summarize_result["response"]
            # st.text_area(label="💫 Initial analysis from DocMind:", value=summary)

# session_id = get_session_id()
# print(f"main {session_id=}")

MODEL_LIST = ["docmind-model"]
model: str = st.selectbox("DocMind Model", options=MODEL_LIST)  # type: ignore

# first turn as Docmind providing initial analysis
default_assistant_prompt = "Let DocMind summarize the document for you."
system_prompt = "😌 Any further questions you'd like to ask about the document?"

st.chat_message("assistant").write(default_assistant_prompt)
doc_summary = initial_analysis["summary"]
doc_context = initial_analysis["context"]
st.chat_message("assistant").write(f"💫 Initial analysis from DocMind:  \n{doc_summary}")

# normal chatting
if st.session_state.file_processed:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": default_assistant_prompt}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        print(f"{prompt=}")
        response = dummy_call_chat(context=doc_summary, prompt=st.session_state.messages)
        # response = send_request(msgs=st.session_state.messages, file=None, session_id=get_session_id())
        msg = response["response"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

