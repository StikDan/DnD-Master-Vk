import json
from abc import ABC, abstractmethod
from db.db_connection import Database
from db.migrations import run_migrations


class BaseImporter(ABC):
    """Базовый класс для импортеров данных"""
    
    def __init__(self):
        self.db = None
    
    async def _load_json(self, file_path: str) -> dict | list:
        """Загружает JSON файл"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def _init_db(self):
        """Инициализирует БД и запускает миграции"""
        async with Database() as db:
            await run_migrations(db)
    
    @abstractmethod
    async def import_data(self, json_file: str) -> str:
        """Основной метод импорта переопределяется в наследниках"""
        pass