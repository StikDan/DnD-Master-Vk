# conversation_history.py
import os
import json
from typing import Optional
from config import Config
from db.db_connection import Database


class ConversationHistory:
    def __init__(self):
        self.history = []
        self.HISTORY_FILE = Config().HISTORY_FILE
        self.MEMORY_PAIR = Config().MEMORY_PAIR
        self._loaded = False


    async def load_history(self):
        """Загружает историю из БД."""
        if self._loaded:
            return

        try:
            async with Database() as db:
                rows = await db.fetchall(
                    "SELECT role, content FROM global_history ORDER BY id ASC"
                )
                self.history = [
                    {"role": row["role"], "content": row["content"]}
                    for row in rows
                ]
                print(f"История загружена из БД: {len(self.history)} сообщений")
                
        except Exception as e:
            print(f"Ошибка загрузки из БД: {e}. Пробуем JSON...")
            try:
                with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.history = loaded if isinstance(loaded, list) else []
            except (FileNotFoundError, json.JSONDecodeError):
                self.history = []
        
        self._loaded = True


    async def add_message(self, role: str, content: str):
        """Добавляет сообщение в БД + в память."""
        if not content or not content.strip():
            return

        message = {
            "role": role.strip().lower(),
            "content": content.strip()
        }
        
        self.history.append(message)
        
        try:
            async with Database() as db:
                await db.execute(
                    "INSERT INTO global_history (role, content) VALUES (?, ?)",
                    (role.strip().lower(), content.strip())
                )
        except Exception as e:
            print(f"Ошибка сохранения в БД: {e}")
            await self._save_json()


    async def delete_message(self, count_msg: int):
        """Удаляет последние N сообщений из БД и памяти."""
        if count_msg <= 0:
            return
        
        if count_msg >= len(self.history):
            self.history = []
        else:
            self.history = self.history[:-count_msg]
        
        try:
            async with Database() as db:
                await db.execute(
                    """DELETE FROM global_history 
                       WHERE id IN (
                           SELECT id FROM global_history ORDER BY id DESC LIMIT ?
                       )""",
                    (count_msg,)
                )
        except Exception as e:
            print(f"Ошибка удаления из БД: {e}")
            await self._save_json()


    async def clear_history(self):
        """Полностью очищает историю из памяти."""
        self.history = []


    async def _save_json(self):
        """Резервное сохранение в JSON (если БД недоступна)."""
        try:
            with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения JSON: {e}")


    def get_last_message(self) -> Optional[dict]:
        if self.history:
            return self.history[-1]
        return None
    
    
    def get_history(self) -> list:
        return self.history[-self.MEMORY_PAIR:]
    
    
    @staticmethod
    def load_prompt(filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Файл промпта {filepath} не найден")
            return ""
        except Exception as e:
            print(f"Ошибка чтения промпта: {e}")
            return ""


    def check_prompt_loaded(self, prompt_path: str) -> str:
        if not os.path.exists(prompt_path):
            return f"Файл промпта {prompt_path} не найден. Сообщений в истории: {len(self.history)}"
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content:
                return f"Промпт загружен ({len(content)} симв.). Сообщений в истории: {len(self.history)}"
            else:
                return f"Файл промпта пуст. Сообщений в истории: {len(self.history)}"
        except Exception as e:
            return f"Ошибка чтения промпта: {e}"