from pathlib import Path
from db.Modules.base_importer import BaseImporter
from db.table_manager import TableManager


class ImportNpc(BaseImporter):
    """Импортер для NPC"""
    
    async def _process_npc_data(self, npc_data, verbose: bool = True) -> tuple[int, int]:
        """Обрабатывает данные NPC и вставляет в БД."""
        imported = 0
        skipped = 0
        
        if isinstance(npc_data, list):
            for npc in npc_data:
                npc_id = await TableManager.insert_npc(npc)
                if npc_id:
                    imported += 1
                    if verbose:
                        print(f"Добавлен NPC: {npc.get('name', 'Без имени')} (ID: {npc_id})")
                else:
                    skipped += 1
                    if verbose:
                        print(f"Пропущен: {npc.get('name', 'Без имени')}")
        
        elif isinstance(npc_data, dict):
            npc_id = await TableManager.insert_npc(npc_data)
            if npc_id:
                imported += 1
                if verbose:
                    print(f"Добавлен NPC: {npc_data.get('name', 'Без имени')} (ID: {npc_id})")
            else:
                skipped += 1
                if verbose:
                    print(f"Пропущен: {npc_data.get('name', 'Без имени')}")
        
        return imported, skipped
    

    async def import_data(self, json_file: str) -> str:
        """Импортирует NPC из JSON файла в базу данных"""
        try:
            npc_data = await self._load_json(json_file)
            await self._init_db()
            
            if not isinstance(npc_data, (list, dict)):
                return "Ошибка: JSON должен содержать объект или массив NPC"
            
            imported, skipped = await self._process_npc_data(npc_data)
            
            if isinstance(npc_data, dict) and skipped > 0:
                return "NPC уже существует (пропущен)"
            
            return f"Загружено {imported} NPC из JSON"

        except Exception as e:
            return f"Ошибка импорта: {e}"
    

    async def import_from_folder(self, folder_path: str) -> str:
        """Импортирует все JSON файлы из папки без повторов"""
        try:
            await self._init_db()
            path = Path(folder_path)
            json_files = list(path.glob("*.json"))
            
            if not json_files:
                return f"В папке {folder_path} не найдено JSON файлов"
            
            total_imported = 0
            total_skipped = 0
            
            for json_file in json_files:
                try:
                    npc_data = await self._load_json(str(json_file))
                    imported, skipped = await self._process_npc_data(npc_data)
                    total_imported += imported
                    total_skipped += skipped
                    
                except Exception as e:
                    print(f"Ошибка в файле {json_file.name}: {e}")
            
            return f"Импортировано: {total_imported} | Пропущено (дубликаты): {total_skipped}"

        except Exception as e:
            return f"Ошибка импорта папки: {e}"
    
    
    # async def reset_table(self):
    #     """Удаляет таблицу npc"""
    #     async with Database() as db:
    #         await db.execute("DROP TABLE IF EXISTS npc")
    #         print("Таблица npc удалена")