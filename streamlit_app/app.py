import streamlit as st
import requests

st.title("LLM based article summary")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input for user query
query = st.chat_input("what do you want?")

if len(str(query)) > 30:
    st.warning("Query length limit exceeded!")

if query:
    try:
        history = st.session_state.messages[-2:]
    except Exception:
        history = {}

    # Make a POST request to the Flask API
    with st.chat_message("user"):
        st.markdown(query)
    
    st.session_state.messages.append({"role":"user", 'content':query})
    
    payload = {
        "query" : query,
        "history" : history
    }
    
    flask_url = "http://localhost:5001/query"
    response = requests.post(flask_url, json=payload)

    if response.status_code == 200:
        with st.chat_message("assistant"):
            answer = response.json().get('response', "No response received.")
            st.session_state.messages.append({"role":'assistant', 'content':answer})
            st.markdown(answer)
    else:
        with st.chat_message("assistant"):
            st.warning(f"{response.status_code}")
            st.session_state.messages.append({'role':'assistant', 'content':response.status_code})
