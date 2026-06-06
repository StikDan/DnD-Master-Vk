import os
from typing import Optional
from .state import State
from .state_config import STATE_FILES


class StateManager:
    def __init__(self, prompts_dir: str = "data/prompts", detect_threshold: int = 5):
        self.prompts_dir = prompts_dir
        self.state = State.NONE
        self._prompt_cache: dict[State, str] = {}
        self._message_count = 0
        self._detect_threshold = detect_threshold
    

    def set_state(self, new_state: State) -> bool:
        """Переключает состояние"""
        if self.state == new_state:
            return False
        
        old_state = self.state
        self.state = new_state
        self._message_count = 0
        self.take_out_cache()

        print(f"Состояние: {old_state.name} -> {new_state.name}")
        return True
    

    def get_state(self) -> State:
        return self.state
    

    def _load_md_file(self, filename: str) -> str:
        """Подгружает содержимое MD-файла"""
        filepath = os.path.join(self.prompts_dir, filename)
        print(f"Поиск файла: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print(f"Загружено: {filename} ({len(content)} симв.)")
                return content
        except FileNotFoundError:
            print(f"Файл не найден: {filename}")
            return ""
        except Exception as e:
            print(f"Ошибка чтения {filename}: {e}")
            return ""
    

    def _build_prompt_for_state(self, state: State) -> str:
        """Собирает промпт для конкретного состояния"""
        if state in self._prompt_cache:
            return self._prompt_cache[state]
        
        files = STATE_FILES.get(state, [])
        sections = []
        
        for filename in files:
            content = self._load_md_file(filename)
            if content:
                sections.append(f"## {filename}\n\n{content}")
        
        prompt = "\n\n---\n\n".join(sections)
        self._prompt_cache[state] = prompt
        return prompt
    

    def get_system_prompt(self) -> str:
        """Возвращает промпт для текущего состояния"""
        return self._build_prompt_for_state(self.state)
    
    def get_system_prompt_for_state(self, state: State) -> str:
        """Возвращает промпт для указанного состояния (не меняя текущее)"""
        return self._build_prompt_for_state(state)
    

    def take_out_cache(self, state: Optional[State] = None):
        """Сбрасывает кэш промптов"""
        if state:
            self._prompt_cache.pop(state, None)
        else:
            self._prompt_cache.clear()


    async def auto_detect_state(self, user_message: str, ollama_client) -> Optional[State]:
        """Авто-детект состояния по сообщению. Возвращает detected state или None."""
        
        self._message_count += 1
        
        message_lower = user_message.lower()
        
        quick_map = {
            State.COMBAT: ["бой", "атакую", "бью", "удар", "враг", "монстр", "сражаюсь", "убить", "атака", "раню", "кричу", "убиваю"],
            State.SOCIAL: ["диалог", "спрашиваю", "говорю", "привет", "кто ты", "расскажи", "диалог", "здравствуй", "болтаю", "торгуюсь", "спросить"],
            State.EXPLORATION: ["исследование", "иду", "смотрю", "осматриваю", "где", "что здесь", "дверь", "комната", "коридор", "ищу", "проверяю", "хожу"],
            State.REST: ["отдых", "отдыхаю", "сплю", "ем", "пью", "лечусь", "привал", "ночую", "пью зелье", "ем еду", "отдых"],
        }
        
        for state, keywords in quick_map.items():
            if any(keyword in message_lower for keyword in keywords):
                if self.state != state:
                    self.set_state(state)
                return state
        
        if self._message_count < self._detect_threshold:
            return None
        
        self._message_count = 0
        
        prompt = f"""
Определи состояние сессии по сообщению игрока.
Варианты: COMBAT, SOCIAL, EXPLORATION, REST, NONE

Сообщение: {user_message}

Ответь ТОЛЬКО одним словом (название состояния).
"""
        
        response = await ollama_client.get_response(prompt, [])
        
        state_map = {
            "COMBAT": State.COMBAT,
            "SOCIAL": State.SOCIAL,
            "EXPLORATION": State.EXPLORATION,
            "REST": State.REST,
        }
        
        detected_state = state_map.get(response.strip().upper(), State.NONE)
        if detected_state != State.NONE and detected_state != self.state:
            self.set_state(detected_state)
            return detected_state
        
        return None
    

    def reset_counter(self):
        """Сбрасывает счётчик сообщений вручную"""
        self._message_count = 0