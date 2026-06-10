from .database import Database
from .Models.player import CREATE_TABLE as CREATE_PLAYER
from .Models.session import CREATE_TABLE as CREATE_SESSION
from .Models.member import CREATE_TABLE as CREATE_MEMBERS
from .Models.character import CREATE_TABLE as CREATE_CHARACTERS
from .Models.npc import CREATE_TABLE as CREATE_NPCS
from .Models.location import CREATE_TABLE as CREATE_LOCATIONS
from .Models.session_history import CREATE_TABLE as CREATE_SESSION_HISTORY
from .Models.inventory import CREATE_TABLE as CREATE_INVENTORY
from .Models.global_history import CREATE_TABLE as CREATE_GLOBAL_HISTORY

# Порядок важен!
CREATE_TABLES = [
    CREATE_PLAYER,                 # 1. Игроки
    CREATE_SESSION,                # 2. Сессии
    CREATE_LOCATIONS,              # 3. Локации (зависят от сессий)
    CREATE_MEMBERS,                # 4. Участники сессий
    CREATE_CHARACTERS,             # 5. Персонажи игроков
    CREATE_NPCS,                   # 6. NPC
    CREATE_SESSION_HISTORY,        # 7. История сессий
    CREATE_INVENTORY,              # 8. Инвентарь
    CREATE_GLOBAL_HISTORY,         # 9. Глобальная история
]


async def run_migrations(db: Database):
    """Выполняет все миграции"""
    for statement in CREATE_TABLES:
        await db.execute(statement)

    await _create_indexes(db)


async def _create_indexes(db: Database):
    """Создаёт индексы для ускорения запросов"""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_session_history_session ON session_history(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_session_history_created ON session_history(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_character_player ON character(player_id)",
        "CREATE INDEX IF NOT EXISTS idx_character_session ON character(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_npc_session ON npc(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_location_session ON location(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_member_session ON member(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_member_player ON member(player_id)",
    ]
    
    for index_sql in indexes:
        await db.execute(index_sql)