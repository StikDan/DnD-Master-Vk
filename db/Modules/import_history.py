from db.Modules.base_importer import BaseImporter
from db.table_manager import TableManager
from db.db_connection import Database

class ImportHistory(BaseImporter):
    """Импортер для истории сообщений"""

    def _parse_message(self, text: str) -> tuple[str, str]:
        """Парсит сообщение из истории"""
        if text.startswith("Мастер:"):
            return "master", text
        elif text.startswith("Игрок "):
            return "player", text
        else:
            return "master", text
    

    async def import_data(self, json_file: str) -> str:
        """Импортирует историю сообщений из JSON файла"""
        try:
            messages = await self._load_json(json_file)
            await self._init_db()
            
            for imported, msg in enumerate(messages):
                role, content = self._parse_message(msg)
                if content:
                    await TableManager.insert_history_row(
                        role=role,
                        content=content
                    )
            
            return f"Загружено {len(messages)} сообщений из JSON | Импортировано {imported+1} сообщений в БД"

        except Exception as e:
            return f"Ошибка импорта: {e}"
    

    async def import_all(self, file_paths: list[str]):
        """Импортирует историю из нескольких файлов"""
        for file_path in file_paths:
            print(f"Загрузка {file_path}...")
            await self.import_data(file_path)
    
    
    async def delete_by_id_range(self, start_id: int, end_id: int):
        """Удаляет сообщения истории по диапазону ID"""
        async with Database() as db:
            await db.execute("DELETE FROM global_history WHERE id BETWEEN ? AND ?", (start_id, end_id))
            print(f"Удалены сообщения с {start_id} по {end_id}")