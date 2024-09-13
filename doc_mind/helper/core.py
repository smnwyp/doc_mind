import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import unquote

import streamlit as st

API_ENDPOINT = "http://ec2-35-158-252-84.eu-central-1.compute.amazonaws.com:8000/generate"

def make_api_call(prompt, file):
    try:
        multipart_data = MultipartEncoder(
            fields={
                'file': ('file.pdf', file, 'application/pdf')
            }
        )

        # Make the API call
        endpoint = f"{API_ENDPOINT}?prompt={unquote(prompt)}"
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
            return None

    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None