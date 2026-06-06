from .database import Database
from .Models.global_history import CREATE_TABLE as CREATE_GLOBAL_HISTORY
from .Models.npc import CREATE_TABLE as CREATE_NPC
from .Models.session import CREATE_TABLE as CREATE_SESSION
from .Models.session_history import CREATE_TABLE as CREATE_SESSION_HISTORY

CREATE_TABLES = [
    CREATE_GLOBAL_HISTORY,
    CREATE_NPC,
    CREATE_SESSION,
    CREATE_SESSION_HISTORY
]


async def run_migrations(db: Database):
    """Выполняет все миграции"""
    for statement in CREATE_TABLES:
        await db.execute(statement)