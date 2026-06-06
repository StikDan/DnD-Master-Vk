import uuid
from typing import Optional, Dict
from .session import Session
from states.state_manager import StateManager
from states.state import State


class SessionManager:
    def __init__(self, prompts_dir: str = "data/prompts"):
        self.sessions: Dict[str, Session] = {}
        self.chat_to_session: Dict[int, str] = {}  # peer_id -> session_id
        self.state_managers: Dict[str, StateManager] = {}  # session_id -> StateManager
        self.prompts_dir = prompts_dir
    
    def create_session(self, session_name = None) -> str:
        session_id = session_name or str(uuid.uuid4())[:8]
        if session_id in self.sessions:
            raise ValueError(f"Сессия {session_id} уже существует")
        
        # Создаём сессию
        self.sessions[session_id] = Session(session_id)
        
        # Создаём StateManager для этой сессии
        self.state_managers[session_id] = StateManager(prompts_dir=self.prompts_dir)
        
        return session_id
    
    def get_session_for_chat(self, peer_id: int) -> Optional[Session]:
        session_id = self.chat_to_session.get(peer_id)
        if session_id:
            return self.sessions.get(session_id)
        return None
    
    def assign_chat_to_session(self, peer_id: int, session_id: str) -> bool:
        if session_id not in self.sessions:
            return False
        
        # Убираем чат из старой сессии
        old_session_id = self.chat_to_session.get(peer_id)
        if old_session_id and old_session_id in self.sessions:
            self.sessions[old_session_id].remove_chat(peer_id)
        
        # Привязываем к новой сессии
        self.sessions[session_id].add_chat(peer_id)
        self.chat_to_session[peer_id] = session_id
        return True
    
    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        for peer_id in session.chat_ids:
            self.chat_to_session.pop(peer_id, None)
        
        del self.sessions[session_id]
        self.state_managers.pop(session_id, None)
        return True
    
    def get_session_state(self, session_id: str) -> State:
        """Получает состояние сессии"""
        state_manager = self.state_managers.get(session_id)
        return state_manager.get_state() if state_manager else State.NONE
    
    def set_session_state(self, session_id: str, new_state: State) -> bool:
        """Устанавливает состояние сессии"""
        state_manager = self.state_managers.get(session_id)
        if not state_manager:
            return False
        
        return state_manager.set_state(new_state)
    
    def get_system_prompt_for_state(self, session_id: str, state: State) -> str:
        """Получает системный промпт для сессии с учётом состояния"""
        state_manager = self.state_managers.get(session_id)
        if not state_manager:
            return ""
        
        return state_manager.get_system_prompt_for_state(state)
    
    def get_current_system_prompt(self, session_id: str) -> str:
        """Получает текущий промпт сессии (для её текущего состояния)"""
        state_manager = self.state_managers.get(session_id)
        if not state_manager:
            return ""
        
        return state_manager.get_system_prompt()
    
    async def auto_detect_state(self, session_id: str, user_message: str, ollama_client) -> Optional[State]:
        """Авто-детект состояния для сессии"""
        state_manager = self.state_managers.get(session_id)
        if not state_manager:
            return None
        
        return await state_manager.auto_detect_state(user_message, ollama_client)
    
    def invalidate_cache(self, session_id: str, state: Optional[State] = None):
        """Сбрасывает кэш промптов для сессии"""
        state_manager = self.state_managers.get(session_id)
        if state_manager:
            state_manager.invalidate_cache(state)