from typing import Optional
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


    async def _retry_message(self, session_id: str):
        """Откатить последних 2 сообщения в сессии"""
        await self.session_history.delete_last_message(session_id, 2)


    async def handle_command(self, message: Message, peer_id: int, text: str) -> bool:
        """
        Обработка команд. Возвращает True, если команда распознана и обработана.
        Возвращает False, если это обычное сообщение.
        """
        if not text or not text.startswith(self.config.IGNORE_PREFIX):
            return False
        
        text_lower = text.lower()
        session = self.session_manager.get_session_for_chat(peer_id)
        session_id = session.session_id if session else None
        
        # !session new [name] — создать новую сессию для этого чата
        if text_lower.startswith(self.config.IGNORE_PREFIX + 'session new'):
            parts = text.split(maxsplit=2)
            name = parts[2] if len(parts) > 2 else None
            new_id = self.session_manager.create_session(name)
            self.session_manager.assign_chat_to_session(peer_id, new_id)
            await message.answer(f"Создана новая сессия: `{new_id}`")
            return True
        
        # !session state [state] — показать/изменить состояние
        if text_lower.startswith(self.config.IGNORE_PREFIX + 'session state'):
            if session is None:
                await message.answer("Нет активной сессии")
                return True
            
            parts = text.split(maxsplit=2)
            if len(parts) > 2:
                # Установка состояния
                state_name = parts[2].upper()
                state_map = {
                    "NONE": State.NONE,
                    "EXPLORATION": State.EXPLORATION,
                    "COMBAT": State.COMBAT,
                    "SOCIAL": State.SOCIAL,
                    "REST": State.REST,
                }
                new_state = state_map.get(state_name)
                if new_state:
                    self.session_manager.set_session_state(session.session_id, new_state)
                    await message.answer(f"Состояние изменено: {new_state.name}")
                else:
                    await message.answer(f"Неверное состояние. Варианты: {list(state_map.keys())}")
            else:
                if session_id:
                    current_state = self.session_manager.get_session_state(session_id)
                    await message.answer(f"Текущее состояние: {current_state.name}")
            return True
        
        # !retry — откатить последний запрос в сессии
        if text_lower == self.config.IGNORE_PREFIX + 'retry':
            if session_id:
                await self._retry_message(session_id)
                await message.answer(f"Откат в сессии `{session_id}` выполнен!")
            else:
                await message.answer("Нет активной сессии")
            return True
        
        # !import-history — импорт истории
        if text_lower == self.config.IGNORE_PREFIX + 'import-history':
            importer = self.import_module.get_importer("history")
            result = await importer.import_data(self.config.HISTORY_FILE)
            await message.answer(result)
            return True
        
        # !import-npcs — импорт NPC
        if text_lower == self.config.IGNORE_PREFIX + 'import-npcs':
            importer = self.import_module.get_importer("npc")
            result = await importer.import_from_folder("data/NPC")
            await message.answer(result)
            return True
        
        # !commands — список команд
        if text_lower == self.config.IGNORE_PREFIX + 'commands':
            await message.answer('''
**Команды сессий:**
`!session new [name]` — создать новую сессию
`!session state [state]` — показать/изменить состояние

**Команды истории:**
`!clear` — очистить историю сессии
`!retry` — откатить последний запрос

**Импорт команды:**
`!import-history` — импортировать историю из JSON
`!import-npcs` — импортировать NPC из папки
            ''')
            return True
        return False