import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

class Config:
    VK_TOKEN = os.environ.get('VK_TOKEN', '')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'deepseek-v3.2:cloud')
    NUM_CTX = 260000
    NUM_PREDICT = 3000
    TEMPERATURE = 0.675
    TOP_P = 0.655
    PROMPT_FILE = os.environ.get('PROMPT_FILE', 'systemPrompt.md')
    HISTORY_FILE = os.environ.get('HISTORY_FILE', 'Legacy.json')
    MEMORY_PAIR = 50
    DB_PATH = Path(os.environ.get("DB_PATH", "./db/pocket_dnd_vk.db"))
    IGNORE_PREFIX = '!'
    SHOW_CURRENT_STATE = False