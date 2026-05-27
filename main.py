import asyncio
from config import Config
from dotenv import load_dotenv
from events import VKBot

# ИНИЦИАЛИЗАЦИЯ
load_dotenv()


config = Config()
vk_bot = VKBot()

asyncio.run(vk_bot.setup())
vk_bot.start()