import streamlit as st
import time
import requests
import os

from dotenv import load_dotenv
load_dotenv()

# 初始化聊天历史
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Streamed response emulator
def response_generator(user_input):

    url = os.environ["API_ENDPOINT"]
    # 将用户输入添加到聊天历史中
    st.session_state['chat_history'].append(f"You: {user_input}")
    # 准备聊天历史参数，这里假设历史记录以逗号分隔
    chat_history_str = ','.join(st.session_state['chat_history'])
    params = {
        "question": user_input,
        "customer_id": "2",
        "chat_history": chat_history_str
    }
    headers = {
        "accept": "application/json"
    }
    response = requests.post(url, params=params, headers=headers)
    
    # 将API的响应添加到聊天历史中
    if response.status_code == 200:
        ai_response = response.json()["answer"]
        st.session_state['chat_history'].append(f"AI: {ai_response}")        
    else:
        ai_response = "AI Error Response"
    
    # for word in ai_response.split():
    #     yield word + " "
    #     time.sleep(0.05)
    return ai_response    


st.title("Chat With Contoso Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Input your question here"):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     response = st.write_stream(response_generator(prompt))
    # # Add assistant response to chat history
    # st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        for chunk in response_generator(prompt).split():
            full_response += chunk + " "
            response_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})