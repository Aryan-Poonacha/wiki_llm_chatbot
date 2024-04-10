import streamlit as st
from vectara_query import VectaraAPI

# Initialize VectaraAPI
vectara_api = VectaraAPI()

# Title
st.title('Yakuza Wiki Chatbot')

# Text input for user query
query_prompt = st.text_input("Enter your query:")
current_conversation_id = ""

# Button to submit query
if st.button('Submit'):
    # Start chat with query
    response_json = vectara_api.chat(query_prompt, current_conversation_id)
    if(current_conversation_id == ""):
        current_conversation_id = response_json['responseSet'][0]['summary'][0]['chat']['conversationId']
    summary_text, top_responses = vectara_api.save_responses(response_json, save_to_file=True)

    # Display summary text
    st.write("Convo ID:", vectara_api.conversation_id)
        # Display summary text
    st.write("Convo ID 2:", current_conversation_id)
    
    # Display summary text
    st.write("Summary:", summary_text)
    
    # Display top responses
    st.write("Top Responses:", top_responses)
