import json
import aiosqlite
from typing import Optional
from pathlib import Path
from config import Config


class SessionHistory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.memory_pairs = Config().MEMORY_PAIR
    

    async def add_session_message(self, session_id: str, role: str, content: str):
        if not content or not content.strip():
            return
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO session_history (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role.strip().lower(), content.strip())
            )
            await db.commit()
    

    async def get_history(self, session_id: str) -> list[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT role, content FROM session_history 
                   WHERE session_id = ? ORDER BY id ASC 
                   LIMIT ? OFFSET (
                       SELECT COUNT(*) FROM session_history WHERE session_id = ?
                   ) - ?""",
                (session_id, self.memory_pairs, session_id, self.memory_pairs)
            )
            rows = await cursor.fetchall()
            return [{"role": row["role"], "content": row["content"]} for row in rows]
    

    async def clear_session(self, session_id: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM session_history WHERE session_id = ?",
                (session_id)
            )
            await db.commit()
    

    async def delete_last_message(self, session_id: str, count: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """DELETE FROM session_history 
                   WHERE id IN (
                       SELECT id FROM session_history 
                       WHERE session_id = ? 
                       ORDER BY id DESC LIMIT ?
                   )""",
                (session_id, count)
            )
            await db.commit()