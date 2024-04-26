import streamlit as st
from Vectara.vectara_query import VectaraAPI
from streamlit_chat import message

# Initialize VectaraAPI
vectara_api = VectaraAPI()

# Title
st.title('Yakuza Wiki Chatbot')

# Chat message handling
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.form("chat_input", clear_on_submit=True):
    user_prompt = st.text_input("Your message:", label_visibility="collapsed")
    if st.form_submit_button("Send"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})

if user_prompt:
    # Start chat with query
    response_json = vectara_api.chat(user_prompt)
    summary_text, top_responses = vectara_api.save_responses(response_json, save_to_file=True)

    # Display summary text
    st.write("Convo ID:", vectara_api.conversation_id)
    
    # Display summary text
    st.write("Summary:", summary_text)
    
    # Display top responses
    for response, score in top_responses.items():
        st.write(f"Response: {response}, Score: {score}")

    st.session_state.messages.append(
        {"role": "assistant", "content": summary_text}
    )

# Display chat messages
for idx, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=f"chat_message_{idx}")
