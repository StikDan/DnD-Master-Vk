import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent / "pocket_dnd_vk.db"


class Database:
    def __init__(self):
        self.db_path = str(DB_PATH)
    
    async def __aenter__(self):
        self.connection = await aiosqlite.connect(self.db_path)
        self.connection.row_factory = aiosqlite.Row
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
    
    async def execute(self, query: str, params: tuple = ()):
        cursor = await self.connection.execute(query, params)
        await self.connection.commit()
        return cursor
    
    async def fetchone(self, query: str, params: tuple = ()):
        cursor = await self.connection.execute(query, params)
        return await cursor.fetchone()
    
    async def fetchall(self, query: str, params: tuple = ()):
        cursor = await self.connection.execute(query, params)
        return await cursor.fetchall()


    async def check_db_initialized(self) -> bool:
        """Проверяет, инициализирована ли база данных."""
        try:
            async with Database() as db:
                result = await db.fetchone(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                if result:
                    print("База данных подключена")
                    return True
                else:
                    print("Таблицы базы данных не найдены")
                    return False
        except Exception as e:
            print(f"Ошибка проверки БД: {e}")
            return False