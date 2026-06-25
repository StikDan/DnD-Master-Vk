import uuid
from typing import Optional, Dict
from .session import Session
from .session_storage import SessionStorage


class SessionManager:
    def __init__(self, db_path: str, prompts_dir: str = "data/prompts"):
        self.storage = SessionStorage(db_path)
        self.sessions: Dict[str, Session] = {}
        self.peer_to_session: Dict[int, str] = {}
        self.session_to_peer: Dict[str, int] = {}  # session_id -> peer_id
        self.prompts_dir = prompts_dir
    

    async def init_db(self):
        """Загружает сессии из БД при старте."""
        await self._load_sessions_from_db()
    

    async def _load_sessions_from_db(self):
        """Загружает все сессии и привязки из БД."""
        sessions_data = await self.storage.load_all_sessions()
        
        for session_id, session_name, peer_id in sessions_data:
            self.sessions[session_id] = Session(session_id, self.prompts_dir)
            
            # Восстанавливаем привязки
            if peer_id is not None:
                self.peer_to_session[peer_id] = session_id
                self.session_to_peer[session_id] = peer_id
    

    def create_session(self, session_name: Optional[str] = None) -> str:
        """Создаёт новую сессию в памяти."""
        session_id = session_name or str(uuid.uuid4())[:8]
        if session_id in self.sessions:
            raise ValueError(f"Сессия {session_id} уже существует")

        self.sessions[session_id] = Session(session_id, self.prompts_dir)
        return session_id
    

    async def create_session_async(self, session_name: Optional[str] = None, peer_id: Optional[int] = None) -> str:
        """Создаёт новую сессию и сохраняет в БД."""
        session_id = self.create_session(session_name)
        await self.storage.save_session(session_id, session_name, peer_id)
        
        if peer_id is not None:
            self.peer_to_session[peer_id] = session_id
            self.session_to_peer[session_id] = peer_id
        
        return session_id
    

    def get_session_by_peer_id(self, peer_id: int) -> Optional[Session]:
        """Получает сессию по ID чата."""
        session_id = self.peer_to_session.get(peer_id)
        if session_id:
            return self.sessions.get(session_id)
        return None
    

    def get_session_by_name(self, session_id: str) -> Optional[Session]:
        """Получает сессию по ID сессии."""
        return self.sessions.get(session_id)
    

    async def assign_chat_to_session(self, peer_id: int, session_id: str) -> bool:
        """Привязывает чат к сессии."""
        if session_id not in self.sessions:
            return False
        
        # Удаляем старую привязку если была
        old_session_id = self.peer_to_session.get(peer_id)
        if old_session_id and old_session_id in self.session_to_peer:
            del self.session_to_peer[old_session_id]
        
        # Создаём новую привязку
        self.peer_to_session[peer_id] = session_id
        self.session_to_peer[session_id] = peer_id
        
        # Сохраняем в БД
        await self.storage.update_session_peer(session_id, peer_id)
        
        return True
    

    async def delete_session(self, session_id: str) -> bool:
        """Удаляет сессию и все привязанные чаты."""
        if session_id not in self.sessions:
            return False
        
        # Удаляем привязку чата
        peer_id = self.session_to_peer.get(session_id)
        if peer_id is not None:
            del self.peer_to_session[peer_id]
            del self.session_to_peer[session_id]
        
        del self.sessions[session_id]
        await self.storage.delete_session(session_id)
        
        return True
    

    def get_all_sessions(self) -> list:
        """Возвращает список всех сессий с информацией."""
        sessions_info = []
        for session_id, session in self.sessions.items():
            peer_id = self.session_to_peer.get(session_id)
            sessions_info.append({
                'id': session_id,
                'peer_id': peer_id,
                'chats_count': 1 if peer_id else 0,
                'state': session.get_state().name if session.get_state() else 'NONE'
            })
        return sessions_info