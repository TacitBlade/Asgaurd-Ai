import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

config = load_config()

GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SERVER_URL = f"http://{os.getenv('HOST', '127.0.0.1')}:{os.getenv('PORT', 8000)}"
