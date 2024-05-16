#load.py

from logic.util import *
from logic.model import *
from logic.database import *


def select_mod(llm_name):
    if llm_name == 'LlaMa2':
        return LLAMA2
    elif llm_name == 'CodeLLaMa':
        return CODELLAMA
    elif llm_name == 'Uncensored LLaMa':
        return UNCENSORE_LLM
    elif llm_name == 'Database':
        return DATABASE
    elif llm_name == 'llama3':
        return DATABASE

@st.cache_resource(experimental_allow_widgets=True)
def load_model():
    llm_name = st.session_state.get('selected_llm', 'LlaMa2')
    model_name = select_mod(llm_name)
    try:
        llm = Ollama(model=model_name)
        return llm
    except Exception as e:
        st.error(f'Failed to load model: {e}')
        return None