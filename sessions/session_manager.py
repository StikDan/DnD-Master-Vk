import uuid
from typing import Optional, Dict
from .session import Session


class SessionManager:
    def __init__(self, prompts_dir: str = "data/prompts"):
        self.sessions: Dict[str, Session] = {}
        self.peer_to_session: Dict[int, str] = {}  # peer_id -> session_id
        self.prompts_dir = prompts_dir
    

    def create_session(self, session_name = None) -> str:
        """Создает новую сессию"""
        session_id = session_name or str(uuid.uuid4())[:8]
        if session_id in self.sessions:
            raise ValueError(f"Сессия {session_id} уже существует")

        self.sessions[session_id] = Session(session_id, self.prompts_dir)
        
        return session_id
    

    def get_session_by_peer_id(self, peer_id: int) -> Optional[Session]:
        """Получает сессию по ID чата"""
        session_id = self.peer_to_session.get(peer_id)
        if session_id:
            return self.sessions.get(session_id)
        return None
    
    
    def get_session_by_name(self, session_id: str) -> Optional[Session]:
        """Получает сессию по ID сессии"""
        return self.sessions.get(session_id)
    
    
    def assign_chat_to_session(self, peer_id: int, session_id: str) -> bool:
        """Привязывает чат к сессии"""
        if session_id not in self.sessions:
            return False
        
        self.peer_to_session[peer_id] = session_id
        return True
    
    
    def delete_session(self, session_id: str) -> bool:
        """Удаляет сессию и все привязанные чаты"""
        if session_id not in self.sessions:
            return False
        
        # Находим и удаляем все чаты этой сессии
        chats_to_remove = [pid for pid, sid in self.peer_to_session.items() if sid == session_id]
        for peer_id in chats_to_remove:
            del self.peer_to_session[peer_id]
        
        del self.sessions[session_id]
        return True