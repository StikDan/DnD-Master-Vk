import os
from typing import Optional
from pathlib import Path
from vkbottle.bot import Bot, Message
from config import Config
from ollama_client import OllamaClient
from utils import Utils
from db.db_connection import Database
from db.migrations import run_migrations
from sessions.session_manager import SessionManager
from sessions.session_history import SessionHistory
from message_handler import MessageHandler
from dotenv import load_dotenv

load_dotenv()
db_path = Path(__file__).parent / "db" / "pocket_dnd_vk.db"


class VKBot:
    def __init__(self):
        self.config = Config()
        self.utils = Utils()
        self.model = OllamaClient()
        self.db = Database()
        self.session_manager = SessionManager(prompts_dir="data/prompts")
        self.session_history: Optional[SessionHistory] = None
        self.handler: Optional[MessageHandler] = None
        
        token = os.environ.get('VK_TOKEN', '')
        self.bot = Bot(token=token)
        
        @self.bot.on.message()
        async def handle_msg(message: Message):
            await self.on_message(message)


    async def setup(self):
        """Асинхронная инициализация перед запуском"""
        print("Проверка таблиц базы данных...")
        async with self.db as db:
            await run_migrations(db)
        print("База данных готова")
        
        self.session_history = SessionHistory(str(db_path))
        
        default_session_id = self.session_manager.create_session("default")
        
        # Создаём обработчик команд
        self.handler = MessageHandler(self.config, self.session_manager, self.session_history)
        
        print('Бот ВК запущен!')
        print(f'Создана сессия по умолчанию: {default_session_id}')


    def start(self):
        """Синхронный запуск бота"""
        self.bot.run_forever()


    async def _get_or_create_session(self, peer_id: int) -> str:
        """
        Получает сессию для чата или создаёт новую.
        Возвращает session_id.
        """
        session = self.session_manager.get_session_for_chat(peer_id)
        
        if session:
            return session.session_id
        
        # Если чат не привязан — создаём новую сессию
        session_id = self.session_manager.create_session()
        self.session_manager.assign_chat_to_session(peer_id, session_id)
        print(f"Чат {peer_id} привязан к сессии {session_id}")
        
        return session_id


    async def on_message(self, message: Message):
        """Обработка входящего сообщения"""
        if self.session_history is None or self.handler is None:
            return
        
        text = message.text or ""
        peer_id = message.peer_id

        is_command = await self.handler.handle_command(message, peer_id, text)
        if is_command:
            return

        session_id = await self._get_or_create_session(peer_id)
        session = self.session_manager.get_session(session_id)
        
        if not session:
            await message.answer("Ошибка сессии. Попробуйте позже.")
            return

        try:
            await self.bot.api.messages.set_activity(
                peer_id=peer_id,
                type='typing'
            )
        except Exception:
            pass
        
        try:
            system_prompt = self.session_manager.get_current_system_prompt(session_id)
            self.model.system_prompt = system_prompt
            
            history = await self.session_history.get_history(session_id)
            
            response = await self.model.get_response(text, history)
            
            try:
                users = await self.bot.api.users.get(user_ids=[message.from_id])
                user_name = users[0].first_name if users else f"User_{message.from_id}"
            except Exception:
                user_name = f"User_{message.from_id}"
            
            await self.session_history.add_session_message(session_id, f"player {user_name}", text)
            await self.session_history.add_session_message(session_id, "master", response)
            
            # Авто-детект состояния
            await self.session_manager.auto_detect_state(session_id, text, self.model)
            
            await self.utils.send_split(self.bot, peer_id, response)
            
        except Exception as e:
            print(f"Ошибка в сессии {session_id}: {e}")
            await message.answer(f"Произошла ошибка: {e}")