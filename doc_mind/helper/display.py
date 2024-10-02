import os

import streamlit as st

# Construct the path to the avatar
avatar_filename = "docmind.jpeg"  # Replace with your actual filename

current_dir = os.path.dirname(os.path.abspath(__file__))
docmind_icon_path = os.path.join(current_dir, "../static", avatar_filename)

user_icon = "❓"
assistant = "assistant"
user = "user"

avatar_profiles = {assistant: docmind_icon_path, user: user_icon}
color_scheme = {assistant: "#008080", user: "#000000"}


def display_message(role: str, message: str):
    st.chat_message(role, avatar=avatar_profiles[role]).markdown(
        f"""
        <div style="color: {color_scheme[role]};">
{message}
</div>
""",
        unsafe_allow_html=True
    )

