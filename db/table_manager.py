import json
from .db_connection import Database


class TableManager:
    @staticmethod
    async def insert_history_row(role: str, content: str) -> int | None:
        async with Database() as db:
            cursor = await db.execute(
                """INSERT INTO global_history (role, content)
                   VALUES (?, ?)""",
                (role, content)
            )
            return cursor.lastrowid
    
    @staticmethod
    async def get_all_history(count_msg: int = 130):
        async with Database() as db:
            rows = await db.fetchall(
                "SELECT * FROM global_history ORDER BY id ASC LIMIT ?",
                (count_msg,)
            )
            return rows
        
    @staticmethod
    async def insert_npc(npc_data: dict) -> int | None:
        """Вставка нового NPC. Возвращает ID или None если NPC уже существует"""
        
        # Разрешённые поля таблицы (новая структура)
        allowed_fields = {
            'name', 'status', 'title', 'age', 'hits',
            'armor', 'inventory', 'strategy', 'weaknesses',
            'companions', 'trophies', 'description_md'
        }
        
        # TEXT-поля
        text_fields = {
            'inventory', 'strategy', 'weaknesses', 'companions', 'trophies', 'description_md'
        }
        
        # Проверяем наличие имени
        npc_name = npc_data.get('name')
        if not npc_name:
            return None
        
        async with Database() as db:
            # Проверяем, существует ли NPC с таким именем
            existing = await db.fetchone(
                "SELECT id_npc FROM npc WHERE name = ?",
                (npc_name,)
            )
            if existing:
                return None
            
            # Фильтруем только разрешённые поля
            columns = []
            values = []
            params = []
            
            for key, value in npc_data.items():
                if key in allowed_fields:
                    columns.append(key)
                    values.append('?')
                    
                    # Обработка значений для TEXT полей
                    if key in text_fields:
                        if value is None:
                            params.append('[]')
                        else:
                            params.append(json.dumps(value, ensure_ascii=False))
                    elif key == 'description_md':
                        params.append(str(value) if value is not None else '')
                    elif key in ('hits', 'armor', 'age'):
                        params.append(value if value is not None else 0)
                    else:
                        params.append(value if value is not None else '')
            
            query = f"""INSERT INTO npc ({', '.join(columns)})
                        VALUES ({', '.join(values)})"""
            
            cursor = await db.execute(query, tuple(params))
            return cursor.lastrowid
        

    @staticmethod
    async def delete_history_rows(count_msg: int) -> bool:
        """Удаляет N записей из global_history"""
        try:
            async with Database() as db:
                await db.execute(
                    """DELETE FROM global_history 
                    WHERE id IN (
                        SELECT id FROM (
                            SELECT id FROM global_history 
                            ORDER BY id DESC 
                            LIMIT ?
                        )
                    )""",
                    (count_msg,)
                )
                return True
        except Exception as e:
            print(f"❌ Ошибка удаления из БД: {e}")
            return False