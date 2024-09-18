import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import uuid

import streamlit as st

from helper.typings import Context, HistoryMessages, ChatResponse, SummarizeResponse


API_ENDPOINT = "http://ec2-35-158-252-84.eu-central-1.compute.amazonaws.com:8000"


def dummy_call_summarize(doc) -> dict:
    return {"summary": "succinct and sensible summary here.", "context": "doc context"}


bad_sumarize_response = SummarizeResponse(response="we are experiencing some problems, "
                                                   "please try again in a few seconds.",
                                          context= Context(tokens=[]))
bad_chat_response = ChatResponse(response="we are experiencing some problems, "
                                          "please try again in a few seconds.")


def call_sumarize(file) -> SummarizeResponse:
    try:
        multipart_data = MultipartEncoder(
            fields={
                'file': ('file.pdf', file, 'application/pdf')
            }
        )

        # Make the API call
        endpoint = f"{API_ENDPOINT}/summarize"

        response = requests.post(
            endpoint,
            data=multipart_data,
            headers={'Content-Type': multipart_data.content_type}
        )

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return bad_sumarize_response

    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return bad_sumarize_response


def call_chat(context: Context, msgs: HistoryMessages) -> ChatResponse:
    try:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # Prepare the data payload
        data = {
            "context": context,
            "msgs": msgs.dict()
        }
        # Make the API call
        endpoint = f"{API_ENDPOINT}/chat"
        response = requests.post(endpoint, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return bad_chat_response

    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return bad_chat_response
