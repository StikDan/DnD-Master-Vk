import aiosqlite
from typing import Optional, Dict, List, Tuple


class SessionStorage:
    """Класс для работы с базой данных сессий."""
    def __init__(self, db_path: str):
        self.db_path = db_path
    

    async def save_session(self, session_id: str, session_name: Optional[str] = None, peer_id: Optional[int] = None):
        """Сохраняет новую сессию в БД."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO session (session_id, session_name, peer_id) VALUES (?, ?, ?)",
                (session_id, session_name, peer_id)
            )
            await db.commit()
    

    async def update_session_peer(self, session_id: str, peer_id: int):
        """Обновляет привязку чата к сессии."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE session SET peer_id = ? WHERE session_id = ?",
                (peer_id, session_id)
            )
            await db.commit()
    

    async def delete_session(self, session_id: str):
        """Удаляет сессию из БД."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM session WHERE session_id = ?", (session_id,))
            await db.commit()
    

    async def load_all_sessions(self) -> List[Tuple[str, Optional[str], Optional[int]]]:
        """Загружает все сессии из БД. Возвращает (session_id, session_name, peer_id)."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT session_id, session_name, peer_id FROM session")
            rows = await cursor.fetchall()
            return [(row["session_id"], row["session_name"], row["peer_id"]) for row in rows]
    

    async def session_exists(self, session_id: str) -> bool:
        """Проверяет, существует ли сессия в БД."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT 1 FROM session WHERE session_id = ?",
                (session_id,)
            )
            row = await cursor.fetchone()
            return row is not None