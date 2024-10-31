import streamlit as st
import requests

st.title("LLM-based RAG Search")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user query
query = st.chat_input("Enter the query: ")

if len(str(query)) > 30:
    st.warning("Query length limit exceeded!")

if query:
    # Make a POST request to the Flask API
    with st.chat_message("user"):
        st.write(query)
    st.session_state.messages.append({"role": "user", "content": query})
    flask_url = "http://localhost:5001/query"
    response = requests.post(flask_url, json={"query": query})

    if response.status_code == 200:
        with st.chat_message("assistant"):
            answer = response.json().get('response', "No response received.")
            st.write("Answer:", answer)
    else:
        with st.chat_message("assistant"):
            print(response.content)
            st.write(f"Error: {response.status_code}")
    st.session_state.messages.append({'role':"assistant", "content":response})
