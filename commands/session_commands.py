from vkbottle.bot import Message
from keyboard import KeyboardBuilder


class SessionCommands:
    """Команды управления сессиями."""
    
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    def register(self) -> dict:
        """Регистрирует команды сессий."""
        return {
            'session new': self.cmd_session_new,
            'session join': self.cmd_session_join,
            'session list': self.cmd_session_list,
            'session state': self.cmd_session_state,
        }
    
    async def cmd_session_new(self, message: Message, peer_id: int, text: str, session):
        """!session new [name] — создать новую сессию"""
        parts = text.split(maxsplit=2)
        name = parts[2] if len(parts) > 2 else None
        
        new_id = self.session_manager.create_session(name)
        self.session_manager.assign_chat_to_session(peer_id, new_id)
        await message.answer(
            f"Создана новая сессия: `{new_id}`",
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )
    
    async def cmd_session_join(self, message: Message, peer_id: int, text: str, session):
        """!session join <id> — присоединиться к сессии"""
        parts = text.split(maxsplit=2)
        
        if len(parts) < 3:
            await message.answer(
                "Использование: `!session join <ID сессии>`\n\n"
                "Пример: `!session join abc12345`",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
            return
        
        session_id = parts[2]
        existing_session = self.session_manager.get_session_by_name(session_id)
        
        if not existing_session:
            await message.answer(
                f"❌ Сессия `{session_id}` не найдена",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
            return
        
        self.session_manager.assign_chat_to_session(peer_id, session_id)
        await message.answer(
            f"✅ Вы присоединились к сессии: `{session_id}`",
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )
    
    async def cmd_session_list(self, message: Message, peer_id: int, text: str, session):
        """!session list — показать все сессии"""
        sessions = self.session_manager.get_all_sessions()
        
        if not sessions:
            await message.answer(
                "📋 Нет активных сессий",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
            return
        
        response = "📋 **Активные сессии**:\n\n"
        for s in sessions:
            current = "📍 " if s['id'] == (session.session_id if session else "") else ""
            response += (
                f"{current}`{s['id']}`\n"
                f"   Чатов: {s['chats_count']} | Состояние: {s['state']}\n\n"
            )
        
        response += "\nДля присоединения: `!session join <ID>`"
        
        await message.answer(
            response,
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )
    
    async def cmd_session_state(self, message: Message, peer_id: int, text: str, session):
        """!session state — текущее состояние"""
        if session is None:
            await message.answer(
                "Нет активной сессии",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
            return
        
        current_state = session.get_state()
        await message.answer(
            f"Текущее состояние: {current_state.name}",
            keyboard=KeyboardBuilder.get_main_keyboard().get_json()
        )