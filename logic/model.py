#model.py

from logic.util import *
from logic.database import *
from logic.query_db import *
from langchain_community.llms import Ollama
import time
import streamlit as st
import uuid
import os
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

current_session_id = None
memory = ConversationBufferWindowMemory(k=2)

def parse_history_file():
    chat_sessions = {}
    current_session_messages = []
    session_id = None

    if not os.path.exists('history.md'):
        open('history.md', 'w', encoding='utf-8').close()

    try:
        with open('history.md', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith('**Session ID:**'):
                if session_id and current_session_messages:
                    chat_sessions[session_id] = current_session_messages
                session_id = line.replace('**Session ID:** ', '')
                current_session_messages = []
            elif '**User**' in line or '**Llama2**' in line:
                role = 'user' if '**User**' in line else 'assistant'
                message = line.replace(f'**{role}**: ', '')
                current_session_messages.append({'role': role, 'content': message})

        if session_id and current_session_messages:
            chat_sessions[session_id] = current_session_messages

    except FileNotFoundError:
        print('The history.md file was not found.')
        chat_sessions = {}

    return chat_sessions

def clear_chat_history():
    global current_session_id
    current_session_id = str(uuid.uuid4())
    with open('history.md', 'a', encoding='utf-8') as f:
        f.write(f'**Session ID:** {current_session_id}\n\n')

    st.session_state.chat_sessions[current_session_id] = []
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def clear_history_file():
    with open('history.md', 'w', encoding='utf-8') as f:
        f.write('')

def get_recent_context(messages, max_messages=50):
    return "\n".join(m['content'] for m in messages[-max_messages:])

def simulate_typing_effect(response, placeholder_text, avatar):
    typed_text = ""
    for i in range(len(response)):
        typed_text += response[i]
        placeholder_text.image(avatar, width=30)
        placeholder_text.markdown(typed_text)
        time.sleep(0.01)

    st.session_state.messages.append({'role': 'assistant', 'content': typed_text})

def process_response(response):
    lines = response.split('\n')
    relevant_lines = [line for line in lines if not any(keyword in line.lower() for keyword in ['product a', 'product b', 'product c', 'details'])]
    filtered_response = '\n'.join(relevant_lines)
    return filtered_response

def save_history(prompt, response, session_id):
    with open('history.md', 'a', encoding='utf-8') as f:
        if not st.session_state.chat_sessions.get(session_id):
            f.write(f'**Session ID:** {session_id}\n')
            st.session_state.chat_sessions[session_id] = [{'role': 'user', 'content': prompt}]
        f.write(f'**User**: {prompt} \n')
        f.write(f'**Llama2**: {response} \n\n')

def process():
    global current_session_id
    from logic.load import load_model
    llama = load_model()

    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 0.70
    if 'top_p' not in st.session_state:
        st.session_state['top_p'] = 1

    if "messages" not in st.session_state.keys() or "session_id" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        current_session_id = str(uuid.uuid4())
        st.session_state["session_id"] = current_session_id

    prompt = st.chat_input("Say Hello!")

    if prompt:
        memory.save_context({"input": prompt}, {"output": ""})
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    for message in st.session_state.messages:
        if message["role"] == 'user':
            avatar = USER_ICON
        else:
            avatar = ASSISTANT_ICON
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

    if prompt:
        context = ""
        full_prompt = f"{context}\nUser: {prompt}"

        generation_settings = {
            'temperature': st.session_state['temperature'],
            'top_p': st.session_state['top_p'],
        }

        with st.spinner(" "):
            start_time = time.time()

            selected_model = st.session_state.get('selected_model', 'llama3')

            response = ""
            if selected_model == 'Database':
                try:
                    response = query_employees(prompt)
                except Exception as e:
                    st.error(f'Error querying database: {e}')
                    response = "An error occurred while querying the database."
            elif selected_model in ['LlaMa2', 'CodeLLaMa', 'Uncensored LLaMa']:
                response = llama(full_prompt, **generation_settings)
            else:
                st.error(f"Unexpected model choice: {selected_model}")
                response = "An error occurred."

            response_time = time.time() - start_time

            if response_time < 2:
                time.sleep(2 - response_time)

        response = process_response(response)
        memory.save_context({"input": prompt}, {"output": response})

        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state['last_response_time'] = f'{response_time:.2f} seconds to respond'

        save_history(prompt, response, st.session_state["session_id"])
        st.rerun()

