from typing import Optional, Callable
from config import Config
from db.Modules import factory_importer
from vkbottle.bot import Message
from sessions.session_manager import SessionManager
from sessions.session_history import SessionHistory
from states.state import State


class MessageHandler:
    def __init__(self, config: Config, session_manager: SessionManager, session_history: SessionHistory):
        self.config = config
        self.session_manager = session_manager
        self.session_history = session_history
        self.import_module = factory_importer
        self._commands = self._register_commands()
    

    def _register_commands(self) -> dict[str, Callable]:
        """Регистрирует доступные команды"""
        return {
            'session new': self._cmd_session_new,
            'session state': self._cmd_session_state,
            'retry': self._cmd_retry,
            'import-history': self._cmd_import_history,
            'import-npcs': self._cmd_import_npcs,
            'commands': self._cmd_commands,
        }
    

    async def _retry_message(self, session_id: str):
        """Откатить последних 2 сообщения в сессии"""
        await self.session_history.delete_last_message(session_id, 2)
    

    async def handle_command(self, message: Message, peer_id: int, text: str) -> bool:
        """
        Обработка команд. Возвращает True, если команда распознана.
        """
        if not text or not text.startswith(self.config.IGNORE_PREFIX):
            return False
        
        command = text[len(self.config.IGNORE_PREFIX):].strip().lower()
        
        for cmd_name, handler in self._commands.items():
            if command == cmd_name or command.startswith(cmd_name + ' '):
                session = self.session_manager.get_session_by_peer_id(peer_id)
                await handler(message, peer_id, text, session)
                return True
        
        return False
    
    
    async def _cmd_session_new(self, message: Message, peer_id: int, text: str, session):
        """!session new [name] — создать новую сессию"""
        parts = text.split(maxsplit=2)
        name = parts[2] if len(parts) > 2 else None
        
        new_id = self.session_manager.create_session(name)
        self.session_manager.assign_chat_to_session(peer_id, new_id)
        await message.answer(f"Создана новая сессия: `{new_id}`")
    

    async def _cmd_session_state(self, message: Message, peer_id: int, text: str, session):
        """!session state [state] — текущее состояние"""
        if session is None:
            await message.answer("Нет активной сессии")
            return
        
        current_state = session.get_state()
        await message.answer(f"Текущее состояние: {current_state.name}")
    

    async def _cmd_retry(self, message: Message, peer_id: int, text: str, session):
        """!retry — откатить последний запрос"""
        if session:
            await self._retry_message(session.session_id)
            await message.answer(f"Откат в сессии `{session.session_id}` выполнен!")
        else:
            await message.answer("Нет активной сессии")
    

    async def _cmd_import_history(self, message: Message, peer_id: int, text: str, session):
        """!import-history — импорт истории"""
        importer = self.import_module.get_importer("history")
        result = await importer.import_data(self.config.HISTORY_FILE)
        await message.answer(result)
    

    async def _cmd_import_npcs(self, message: Message, peer_id: int, text: str, session):
        """!import-npcs — импорт NPC"""
        importer = self.import_module.get_importer("npc")
        result = await importer.import_from_folder("data/NPC")
        await message.answer(result)
    

    async def _cmd_commands(self, message: Message, peer_id: int, text: str, session):
        """!commands — список команд"""
        await message.answer('''
Команды сессий:
`!session new [name]` — создать новую сессию
`!session state [state]` — показать текущее состояние

**Команды истории:**
`!clear` — очистить историю сессии
`!retry` — откатить последний запрос

**Импорт команды:**
`!import-history` — импортировать историю из JSON
`!import-npcs` — импортировать NPC из папки
        ''')