import asyncio
from dotenv import load_dotenv
from events import VKBot

# ИНИЦИАЛИЗАЦИЯ
load_dotenv()


vk_bot = VKBot()

asyncio.run(vk_bot.setup())
vk_bot.start()