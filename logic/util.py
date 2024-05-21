#util.py
from dotenv import load_dotenv, get_key
import os



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)

PASS = get_key(dotenv_path, 'PASS')
DATABASE_NAME = 'omnidata'

CENTERED = 'centered'
WIDE = 'wide'


CODEBONGA = 'codebbonga'
CODELLAMA = 'codellama'
LLAMA2 = 'llama2-uncensored'
UNCENSORE_LLM = 'uncensored_llm'
DATABASE = 'codellama'
LLAMA3 = 'llama3'

USER_ICON = '/Volumes/Samsung 970 EVO/Documents/Python/Llama2/icons/vector60-5502-01.jpg'
ASSISTANT_ICON = '/Volumes/Samsung 970 EVO/Documents/Python/Llama2/icons/XZ, ZX, X AND Z Abstract initial monogram letter alphabet logo design.png'