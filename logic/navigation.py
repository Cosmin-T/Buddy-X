#navigation.py

from logic.model import *
from logic.util import *
from logic.database import *
import streamlit as st
import time

def side():
    with st.sidebar:
        if 'last_response_time' in st.session_state:
            st.info(st.session_state['last_response_time'])
        col1, col2 = st.columns([1, 8])

        col1.image(ASSISTANT_ICON, width=40)

        col2.subheader('Chat')

        for _ in range(2):
            st.write('\n')

        st.button(':heavy_plus_sign: New Chat', on_click=clear_chat_history)

        if 'chat_sessions' not in st.session_state:
            st.session_state.chat_sessions = parse_history_file()

        if 'chat_sessions' in st.session_state and st.session_state.chat_sessions:
            with st.container(height=400):
                for session_index, (session_key, session_messages) in enumerate(st.session_state.chat_sessions.items()):
                    first_user_message = "No user messages"
                    for m in session_messages:
                        if m['role'] == 'user':
                            first_user_message = m['content']
                            break

                    words = first_user_message.split()
                    if len(words) > 10:
                        button_label = ' '.join(words[:10]) + "..."
                    else:
                        button_label = ' '.join(words)

                    if st.button(button_label, key=session_key):
                        st.session_state.messages = session_messages
                        st.rerun()

        if 'chat_sessions' in st.session_state and st.session_state.chat_sessions:
            if st.button("Clear History", on_click=clear_history_file):
                st.session_state.chat_sessions.clear()
                st.rerun()

        for _ in range(2):
            st.write('\n')

        temperature = st.slider('Temperature', min_value=0.01, max_value=1.5, value=0.70, step=0.01)
        if temperature:
            temp = st.info(f'Set')
            temp.empty()
        top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=1.0, step=0.01)
        if top_p:
            topp =st.info(f'Set')
            topp.empty()

        for _ in range(2):
            st.write('\n')

        model_choice = st.selectbox(
            'Select LLM:',
            ('LlaMa2', 'CodeLLaMa', 'Uncensored LlaMa', 'Database'),
            key='model_choice'
        )

        st.session_state['selected_model'] = model_choice

        # for _ in range(2):
        #     st.write('\n')

        # # connection = connect_to_database()
        # # database_choice = st.selectbox(
        # #     'Select Version',
        # #     ('Database V', 'Chat V'),
        # #     key='database_choice'
        # # )
        # # if database_choice == 'Chat V':
        # #     close_database_connection(connection)
        # # if database_choice == 'Database V':
        # #     connection
        # #     add_random_employee(connection)