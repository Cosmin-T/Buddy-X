from dotenv import load_dotenv, get_key
import os



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv(dotenv_path, 'BOT_TOKEN')
APP_TOKEN = os.getenv(dotenv_path, 'APP_TOKEN')