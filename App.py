import os
import json
import logging
import requests
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import base64

load_dotenv()

def get_latest_conversation_id(api_key, customer_id):
    """Retrieves the latest conversation ID from Vectara."""
    response = requests.post(
        "https://api.vectara.io/v1/list-conversations",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "customer-id": customer_id,
            "x-api-key": api_key,
        },
        data=json.dumps({"numResults": 0, "pageKey": ""}),
    )
    response_data = response.json()
    return (
        response_data["conversation"][-1]["conversationId"]
        if response_data and "conversation" in response_data
        else None
    )


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


st.session_state["corpus_number"] = st.secrets["VECTARA_CORPUS_ID"]
st.session_state["vectara_api_key"] = st.secrets["VECTARA_API_KEY"]
st.session_state["vectara_customer_id"] = st.secrets["VECTARA_CUSTOMER_ID"]

# Streamlit page configuration
st.set_page_config(page_title="Yakuza Chatbot", page_icon="⛩️")

set_png_as_page_bg('assets/background.png')

# Add logo and title
st.image("assets/logo.png", use_column_width=True)
st.title("Yakuza Chatbot")
st.markdown("Ask me any questions about anything and everything Yakuza!")

# Chat message handling
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.form("chat_input", clear_on_submit=True):
    user_prompt = st.text_input("Your message:", label_visibility="collapsed")
    if st.form_submit_button("Send"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})

if user_prompt and st.session_state["vectara_api_key"]:
    conversation_id = get_latest_conversation_id(
        st.session_state["vectara_api_key"], st.session_state["vectara_customer_id"]
    )
    response = requests.post(
        "https://api.vectara.io/v1/query",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "customer-id": st.session_state["vectara_customer_id"],
            "x-api-key": st.session_state["vectara_api_key"],
        },
        data=json.dumps(
            {
                "query": [
                    {
                        "query": user_prompt,
                        "start": 0,
                        "numResults": 3,
                        "contextConfig": {
                            "sentences_before": 3,
                            "sentences_after": 3,
                            "start_tag": "<response>",
                            "end_tag": "</response>",
                        },
                        "corpusKey": [{"corpus_id": st.session_state["corpus_number"]}],
                        "summary": [
                            {"max_summarized_results": 3, "response_lang": "en"}
                        ],
                        "chat": {"store": True, "conversationId": conversation_id},
                    }
                ]
            }
        ),
    )
    query_response = response.json()

    if query_response["responseSet"] and query_response["responseSet"][0]["response"]:
        score = query_response["responseSet"][0]["response"][0]["score"]
        first_response = query_response["responseSet"][0]["summary"][0]["text"]

        if (
            score < 0.65
            or "The returned results did not contain sufficient information"
            in first_response
        ):
            st.write("I'm not sure I have enough information to provide an answer to that question.")

        st.session_state.messages.append(
            {"role": "assistant", "content": first_response}
        )

# Display chat messages
for idx, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=f"chat_message_{idx}")
