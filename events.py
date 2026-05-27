import os
from vkbottle.bot import Bot, Message
from config import Config
from ollama_client import OllamaClient
from conversation_history import ConversationHistory
from utils import Utils
from db.db_connection import Database
from session_state.state_manager import StateManager
from message_handler import MessageHandler
from dotenv import load_dotenv

load_dotenv()


class VKBot:
    def __init__(self):
        self.config = Config()
        self.history = ConversationHistory()
        self.utils = Utils()
        self.state = StateManager()
        self.model = OllamaClient()
        self.db = Database()
        self.handler = MessageHandler(self.config, self.history)
        
        token = os.environ.get('VK_TOKEN', '')
        self.bot = Bot(token=token)
        
        @self.bot.on.message()
        async def handle_msg(message: Message):
            await self.on_message(message)


    async def setup(self):
        """Асинхронная инициализация перед запуском"""
        await self.db.check_db_initialized()
        await self.history.load_history()
        print(self.history.check_prompt_loaded(self.config.PROMPT_FILE))
        print('Бот ВК запущен!')

    def start(self):
        """Синхронный запуск бота"""
        self.bot.run_forever()


    async def on_message(self, message: Message):
        """Обработка входящего сообщения"""
        text = message.text or ""
        is_command = await self.handler.handle_command(message)
        if is_command:
            return

        try:
            await self.bot.api.messages.set_activity(
                peer_id=message.peer_id,
                type='typing'
            )
        except Exception:
            pass
        try:
            system_prompt = self.state.get_system_prompt()
            self.model.system_prompt = system_prompt
            
            response = await self.model.get_response(
                text,
                self.history.get_history()
            )
            try:
                users = await self.bot.api.users.get(user_ids=[message.from_id])
                user_name = users[0].first_name if users else f"User_{message.from_id}"
            except Exception:
                user_name = f"User_{message.from_id}"
            
            await self.history.add_message(f"player {user_name}", text)
            await self.history.add_message("master", response)
            
            await self.utils.send_split(self.bot, message.peer_id, response)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            await message.answer(f"Произошла ошибка: {e}")