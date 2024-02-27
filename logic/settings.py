#settings.py

import streamlit as st

def apply_settings(page_title, layout):
    st.set_page_config(page_title=page_title,layout=layout)
    # st.title(f"{page_title} ")

    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    custom_css = """
    <style>
        body {
            background-color: #171717;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #999;
            font-weight: 500;
            transition: color 0.3s;
        }
        .stApp {
            background: linear-gradient(-199deg, #171717 5%, #0e0e0e 40%);
            border-radius: 10px;
            box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.3);
            padding: 50px;
        }
         button[data-testid="baseButton-secondary"] {
         background-color: #newColor;
         color: #FFF;
         border: none;
         border-radius: 12px;
         }

         button[data-testid="baseButton-secondary"]:hover {
             background-color: #newColorLighter;
         }

         button[data-testid="baseButton-secondaryFormSubmit"] {
             background-color: #063b3f;
             color: #FFF;
             border: none;
             border-radius: 12px;
         }

         button[data-testid="baseButton-secondaryFormSubmit"]:hover {
             background-color: #172a2b;
         }
         .st-emotion-cache-1wmy9hl e1f1d6gn0 {
             border: none;
             background: transparent;
             margin: 0;
             padding: 0;
        }
        .stChatFloatingInputContainer {
            border: none;
            background-color: #0e0e0e;
        }
        .st-emotion-cache-16txtl3 {
            border: none;
            background-color: #0e0e0e;
        }
        .st-emotion-cache-1ec6rqw {
            border: none;
            background-color: #0e0e0e;
        }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)