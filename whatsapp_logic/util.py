from dotenv import load_dotenv, get_key
import os



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
APP_SECRET = os.getenv('APP_SECRET')
RECIPIENT_WAID = os.getenv('RECIPIENT_WAID')
VERSION = os.getenv('VERSION')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')