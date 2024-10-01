import streamlit as st

from helper.core import call_sumarize, call_chat
from helper.typings import Context, HistoryMessages, Message
from component.sidebar import sidebar

docmind_icon_path = "./static/docmind.jpeg"
user_icon = "❓"
assistant = "assistant"
user = "user"
avatar_profiles = {assistant: docmind_icon_path, user: user_icon}

st.set_page_config(page_title="DocMind", page_icon="📖", layout="wide")

col1, col2 = st.columns([1, 6])  # Adjust the ratio as needed
with col1:
    st.header("DocMind")
with col2:
    st.image(docmind_icon_path, width=50)

# st.chat_message("assistant", avatar=docmind_icon_path).write(f"please upload your PDF or image file from the sidebar ↢↢. "
#                                    f"\nDocMind will perform its magic after that.")
st.chat_message("assistant", avatar=docmind_icon_path).markdown(
    f"""
    <div style="color: #008080;">
        Please upload your PDF or image file from the sidebar on the left 👈🏻
        <br>
        DocMind will perform its magic after that.
    </div>
    """,
    unsafe_allow_html=True
)

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

st.chat_message(assistant, avatar=avatar_profiles[assistant]).write(default_assistant_prompt)
st.chat_message(assistant, avatar=avatar_profiles[assistant]).write(f"💫 Initial analysis from DocMind:  \n{st.session_state.summary}")

# normal chatting
if "messages" not in st.session_state:
    st.session_state["messages"] = [Message(role="assistant", content=default_assistant_prompt)]

for msg in st.session_state.messages.msgs:
    st.chat_message(msg.role, avatar=avatar_profiles[msg.role]).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.msgs.append(Message(role="user", content=prompt))
    st.chat_message(user, avatar=avatar_profiles[user]).write(prompt)
    chat_response = call_chat(context=st.session_state.context, msgs=st.session_state.messages)
    msg = chat_response["response"]
    st.session_state.messages.msgs.append(Message(role="assistant", content=msg))
    st.chat_message(assistant, avatar=avatar_profiles[assistant]).write(msg)


