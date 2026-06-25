# message_handler.py
from typing import Callable
from config import Config
from db.Modules import factory_importer
from vkbottle.bot import Message
from sessions.session_manager import SessionManager
from sessions.session_history import SessionHistory
from keyboard import KeyboardBuilder
from commands import SessionCommands, DiceCommands


class MessageHandler:
    def __init__(self, config: Config, session_manager: SessionManager, session_history: SessionHistory):
        self.config = config
        self.session_manager = session_manager
        self.session_history = session_history
        self.import_module = factory_importer
        
        # Инициализируем модули команд
        self.session_commands = SessionCommands(session_manager)
        self.dice_commands = DiceCommands()
        
        # Словарь для хранения ожидающих действий
        self._pending_actions: dict[int, str] = {}

        # Регистрируем все команды
        self._commands = self._register_commands()
    

    def _register_commands(self) -> dict[str, Callable]:
        """Регистрирует все команды"""
        commands = {}
        commands.update(self.session_commands.register())
        commands.update(self.dice_commands.register())
        commands.update({
            'retry': self._cmd_retry,
            'import-history': self._cmd_import_history,
            'import-npcs': self._cmd_import_npcs,
            'commands': self._cmd_commands,
        })
        return commands
    

    async def _retry_message(self, session_id: str):
        """Откатить последних 2 сообщения в сессии"""
        await self.session_history.delete_last_message(session_id, 2)


    async def handle_command(self, message: Message, peer_id: int, text: str) -> bool:
        """Обработка команд. Возвращает True, если команда распознана."""
        
        if peer_id in self._pending_actions:
            action = self._pending_actions.pop(peer_id)
            if action == 'session new':
                if text.startswith(self.config.IGNORE_PREFIX):
                    return False
                
                await self.session_commands.cmd_session_new_text(message, peer_id, text)
                return True

        if not text or not text.startswith(self.config.IGNORE_PREFIX):
            return False
        
        command = text[len(self.config.IGNORE_PREFIX):].strip().lower()
        
        for cmd_name, handler in self._commands.items():
            if command == cmd_name or command.startswith(cmd_name + ' '):
                session = self.session_manager.get_session_by_peer_id(peer_id)
                await handler(message, peer_id, text, session)
                return True
        
        return False
    
    
    async def handle_payload(self, message: Message, peer_id: int, payload: dict) -> bool:
        """Обработка payload от кнопок."""
        if not payload:
            return False
        
        # Сначала проверяем кубики
        if await self.dice_commands.handle_payload(message, peer_id, payload):
            return True
        
        # Обработка команд из кнопок
        if 'command' in payload:
            command = payload['command']
            
            # Обработка новой сессии
            if command == 'session new':
                self._pending_actions[peer_id] = 'session new'
                await message.answer(
                    "Введите имя для новой сессии:",
                    keyboard=KeyboardBuilder.get_main_keyboard().get_json()
                )
                return True

            text = f"{self.config.IGNORE_PREFIX}{command}"
            return await self.handle_command(message, peer_id, text)
        
        return False
    
    
    async def _cmd_session_new(self, message: Message, peer_id: int, text: str, session):
        """!session new [name] — создать новую сессию"""
        await self.session_commands.cmd_session_new(message, peer_id, text, session)
    

    async def _cmd_session_state(self, message: Message, peer_id: int, text: str, session):
        """!session state — текущее состояние"""
        await self.session_commands.cmd_session_state(message, peer_id, text, session)
    

    async def _cmd_retry(self, message: Message, peer_id: int, text: str, session):
        """!retry — откатить последний запрос"""
        if session:
            await self._retry_message(session.session_id)
            await message.answer(
                f"Откат в сессии `{session.session_id}` выполнен!",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
        else:
            await message.answer(
                "Нет активной сессии",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
    

    async def _cmd_import_history(self, message: Message, peer_id: int, text: str, session):
        """!import-history — импорт истории"""
        importer = self.import_module.get_importer("history")
        result = await importer.import_data(self.config.HISTORY_FILE)
        await message.answer(
            result,
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )


    async def _cmd_import_npcs(self, message: Message, peer_id: int, text: str, session):
        """!import-npcs — импорт NPC"""
        importer = self.import_module.get_importer("npc")
        result = await importer.import_from_folder("data/NPC")
        await message.answer(
            result,
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )
    

    async def _cmd_commands(self, message: Message, peer_id: int, text: str, session):
        """!commands — список команд"""
        await message.answer(
            '''
Команды сессий:
`!session new [name]` — создать новую сессию
`!session list` — показать все сессии
`!session join [id]` — присоединиться к сессии
`!session state` — показать текущее состояние

Броски:
`!dice` — показать клавиатуру с кубиками

Команды истории:
`!clear` — очистить историю сессии
`!retry` — откатить последний запрос
        ''',
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )