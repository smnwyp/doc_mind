import os

import streamlit as st

from helper.core import call_chat
from helper.display import display_message, user, assistant, docmind_icon_path
from helper.typings import Context, HistoryMessages, Message
from component.sidebar import sidebar


st.set_page_config(page_title="DocMind", page_icon="📖", layout="wide")

col1, col2 = st.columns([1, 6])  # Adjust the ratio as needed
with col1:
    st.header("DocMind")
with col2:
    st.image(docmind_icon_path, width=50)

instruction = """Please upload your PDF or image file from the sidebar on the left 👈🏻
<br>
DocMind will perform its magic after that."""
display_message(role=assistant, message=instruction)

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

display_message(role=assistant, message=default_assistant_prompt)
display_message(role=assistant, message=f"💫 Initial analysis from DocMind:  \n{st.session_state.summary}")

# normal chatting
if "messages" not in st.session_state:
    st.session_state["messages"] = [Message(role="assistant", content=default_assistant_prompt)]

for msg in st.session_state.messages.msgs:
    display_message(role=msg.role, message=msg.content)

if prompt := st.chat_input():
    st.session_state.messages.msgs.append(Message(role="user", content=prompt))
    display_message(role=user, message=prompt)
    chat_response = call_chat(context=st.session_state.context, msgs=st.session_state.messages)
    msg = chat_response["response"]
    st.session_state.messages.msgs.append(Message(role="assistant", content=msg))
    display_message(role=assistant, message=msg)


