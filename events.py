import os
import json
from typing import Optional
from pathlib import Path
from vkbottle.bot import Bot, Message
from config import Config
from ollama_client import OllamaClient
from utils import Utils
from db.database import Database
from db.migrations import run_migrations
from sessions.session_manager import SessionManager
from sessions.session_history import SessionHistory
from message_handler import MessageHandler
from keyboard import KeyboardBuilder


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
        
        self.session_history = SessionHistory(str(self.config.DB_PATH))
        
        default_session_id = self.session_manager.create_session("default")

        self.handler = MessageHandler(self.config, self.session_manager, self.session_history)
        
        print('Бот ВК запущен!')
        print(f'Создана сессия по умолчанию: {default_session_id}')


    def start(self):
        """Синхронный запуск бота"""
        self.bot.run_forever()


    async def on_message(self, message: Message):
        """Обработка входящего сообщения"""
        if self.session_history is None or self.handler is None:
            return
        
        text = message.text or ""
        peer_id = message.peer_id

        # Проверка нажатия кнопки
        if message.payload:
            await self._handle_button(message, peer_id)
            return

        # Проверка текстовых команд
        is_command = await self.handler.handle_command(message, peer_id, text)
        if is_command:
            return

        # Получение сессии
        session_id, session = await self._get_or_create_session(peer_id)
        
        if not session:
            await message.answer("Ошибка сессии. Попробуйте позже.")
            return

        try:
            await self._show_typing(peer_id)
            
            system_prompt = self._get_system_prompt(session)
            history = await self._get_history(session_id)
            response = await self._get_model_response(text, history, system_prompt)
            user_name = await self._get_user_name(message.from_id)

            await self._save_messages(session_id, user_name, text, response)
            await self._update_state(session, text)
            
            await self._send_response(peer_id, response)
            
        except Exception as e:
            print(f"Ошибка в сессии {session_id}: {e}")
            await message.answer(f"Произошла ошибка: {e}")


    async def _handle_button(self, message: Message, peer_id: int):
        """Обработка нажатия на кнопку"""
        if self.handler is None:
            print("Handler ещё не инициализирован")
            return
        
        payload = message.payload
        if not payload:
            return
        
        try:
            if isinstance(payload, str):
                payload = json.loads(payload)
        except (json.JSONDecodeError, TypeError):
            print(f"Ошибка JSON payload: {payload}")
            return
        
        if not isinstance(payload, dict):
            return
        
        await self.handler.handle_payload(message, peer_id, payload)


    async def _get_or_create_session(self, peer_id: int):
        session = self.session_manager.get_session_by_peer_id(peer_id)
        if session:
            return session.session_id, session
        
        session_id = self.session_manager.create_session()
        self.session_manager.assign_chat_to_session(peer_id, session_id)
        session = self.session_manager.get_session_by_name(session_id)
        
        print(f"Чат {peer_id} создан. ID сессии: {session_id}")
        return session_id, session


    async def _show_typing(self, peer_id: int):
        try:
            await self.bot.api.messages.set_activity(peer_id=peer_id, type='typing')
        except Exception:
            pass


    def _get_system_prompt(self, session) -> str:
        system_prompt = session.get_system_prompt()
        self.model.system_prompt = system_prompt
        return system_prompt


    async def _get_history(self, session_id: str) -> list:
        if self.session_history is None:
            return []
        return await self.session_history.get_history(session_id)


    async def _get_model_response(self, text: str, history: list, system_prompt: str) -> str:
        return await self.model.get_response(text, history)


    async def _get_user_name(self, user_id: int) -> str:
        try:
            users = await self.bot.api.users.get(user_ids=[user_id])
            if users and users[0].first_name:
                return users[0].first_name
            return f"User_{user_id}"
        except Exception:
            return f"User_{user_id}"


    async def _save_messages(self, session_id: str, user_name: str, user_text: str, bot_response: str):
        if self.session_history is None:
            return
        await self.session_history.add_session_message(session_id, f"player {user_name}", user_text)
        await self.session_history.add_session_message(session_id, "master", bot_response)


    async def _update_state(self, session, text: str):
        await session.auto_detect_state(text, self.model)


    async def _send_response(self, peer_id: int, response: str):
        await self.utils.send_split(self.bot, peer_id, response, keyboard=KeyboardBuilder.get_main_keyboard())