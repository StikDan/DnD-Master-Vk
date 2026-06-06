from typing import Optional
from states.state import State


class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = State.NONE
        self.history: list[dict] = []
        self.chat_ids: set[int] = set()  # peer_id чатов, привязанных к сессии
        self._message_count = 0
        self.active = True
    
    def add_chat(self, peer_id: int):
        self.chat_ids.add(peer_id)
    
    def remove_chat(self, peer_id: int):
        self.chat_ids.discard(peer_id)
    
    def has_chat(self, peer_id: int) -> bool:
        return peer_id in self.chat_ids