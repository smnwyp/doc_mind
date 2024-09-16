import requests
import json
from typing import List, Dict
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import unquote
import uuid

import streamlit as st

# API_ENDPOINT = "http://ec2-35-158-252-84.eu-central-1.compute.amazonaws.com:8000/generate"

def get_session_id(creat_new: bool=False):
    if creat_new or 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id


def dummy_call_summarize(doc) -> dict:
    print(f"-- summarize called!")
    return {"summary": "succinct and sensible summary here.", "context": "doc context"}


def dummy_call_chat(context: str, prompt: List[dict]) -> dict:
    print(f"---- chat called!")
    return {"response": f"regarding your query: '{prompt}', \nsth sensible here!"}

#
# def make_api_call(prompt, session_id: str, file=None):
#     try:
#         multipart_data = MultipartEncoder(
#             fields={
#                 'file': ('file.pdf', file, 'application/pdf')
#             }
#         )
#
#         # Make the API call
#         print(prompt)
#         endpoint = f"{API_ENDPOINT}?prompt={unquote(prompt)}"
#
#         response = requests.post(
#             endpoint,
#             data=multipart_data,
#             headers={'Content-Type': multipart_data.content_type}
#         )
#
#         # Check if the request was successful
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error(f"Error: {response.status_code} - {response.text}")
#             return None
#
#     except requests.RequestException as e:
#         st.error(f"An error occurred: {e}")
#         return None
#
#
# def send_request(msgs: List[Dict], session_id: str, file=None):
#     data = {
#         "request": json.dumps({"msgs": msgs,
#                                "session_id": session_id})
#     }
#
#     # Prepare the file
#     files = {
#         "file": file
#     }
#
#     # Send the POST request
#     # response = requests.post(API_ENDPOINT, data=data, files=files)
#     dummy_response = msgs[-1]["content"]
#     response = {"response": f"about your question '{dummy_response}', here's sth sensible!"}
#
#     return response