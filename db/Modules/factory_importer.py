from db.Modules.import_npc import ImportNpc
from db.Modules.import_history import ImportHistory


def get_importer(data_type: str):
    """Фабрика для создания импортера по типу данных"""
    importers = {
        "npc": ImportNpc,
        "history": ImportHistory,
    }
    
    if data_type not in importers:
        raise ValueError(f"Неизвестный тип: {data_type}. Доступные: {list(importers.keys())}")
    
    return importers[data_type]()