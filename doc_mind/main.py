import streamlit as st

from helper.core import call_sumarize, call_chat
from helper.typings import Context, HistoryMessages, Message
from component.sidebar import sidebar

st.set_page_config(page_title="DocMind", page_icon="📖", layout="wide")
st.header("DocMind 🧠")

st.chat_message("assistant").write(f"please upload your PDF or image file from the sidebar ⬅️. "
                                   f"\nDocMind will perform its magic after that.")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = HistoryMessages(msgs=[])
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False
if 'context' not in st.session_state:
    st.session_state.context = Context()
if 'summary' not in st.session_state:
    st.session_state.summary = None


sidebar()


def start_new_session():
    st.session_state.messages = HistoryMessages(msgs=[])
    st.session_state.file_processed = False
    st.session_state.context = Context()
    st.session_state.summary = None


if st.sidebar.button("Read a new document"):
    start_new_session()
    st.sidebar.success("New doc same DocMind!")
    st.rerun()


MODEL_LIST = ["docmind-model"]
model: str = st.selectbox("DocMind Model", options=MODEL_LIST)  # type: ignore

# first turn as Docmind providing initial analysis
default_assistant_prompt = "Let DocMind summarize the document for you."

st.chat_message("assistant").write(default_assistant_prompt)
st.chat_message("assistant").write(f"💫 Initial analysis from DocMind:  \n{st.session_state.summary}")

# normal chatting
if "messages" not in st.session_state:
    st.session_state["messages"] = [Message(role="assistant", content=default_assistant_prompt)]

for msg in st.session_state.messages.msgs:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.msgs.append(Message(role="user", content=prompt))
    st.chat_message("user").write(prompt)
    chat_response = call_chat(context=st.session_state.context, msgs=st.session_state.messages)
    msg = chat_response["response"]
    st.session_state.messages.msgs.append(Message(role="assistant", content=msg))
    st.chat_message("assistant").write(msg)


