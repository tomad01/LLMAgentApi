import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(os.path.dirname(__file__)).parent / ".env"
load_dotenv(dotenv_path)

EMAILS_TXT = os.environ['EMAILS_TXT']
QDRANT_EMAILS = os.environ["QDRANT_EMAILS"]

CHATS_TXT = os.environ['CHATS_TXT']
QDRANT_CHATS = os.environ["QDRANT_CHATS"]


