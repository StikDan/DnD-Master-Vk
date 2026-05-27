from .db_connection import Database
from .Models.global_history import CREATE_TABLE as CREATE_GLOBAL_HISTORY
from .Models.npc import CREATE_TABLE as CREATE_NPC


CREATE_TABLES = [
    CREATE_GLOBAL_HISTORY,
    CREATE_NPC,
]


async def run_migrations(db: Database):
    """Выполняет все миграции"""
    for statement in CREATE_TABLES:
        await db.execute(statement)