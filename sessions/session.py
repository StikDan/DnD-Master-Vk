from typing import Optional
from states.state import State
from states.state_manager import StateManager


class Session:
    def __init__(self, session_id: str, prompts_dir: str = "data/prompts"):
        self.session_id = session_id
        self.state_manager = StateManager(prompts_dir)

    
    def get_state(self) -> State:
        """Получает текущее состояние сессии"""
        return self.state_manager.get_state()
    

    def set_state(self, new_state: State) -> bool:
        """Устанавливает состояние сессии"""
        return self.state_manager.set_state(new_state)
    

    def get_system_prompt(self) -> str:
        """Получает системный промпт для текущего состояния"""
        return self.state_manager.get_system_prompt()
    

    def get_system_prompt_for_state(self, state: State) -> str:
        """Получает промпт для указанного состояния"""
        return self.state_manager.get_system_prompt_for_state(state)
    
    
    async def auto_detect_state(self, user_message: str, ollama_client) -> Optional[State]:
        """Авто-детект состояния по сообщению"""
        return await self.state_manager.auto_detect_state(user_message, ollama_client)
    

    def take_out_cache(self, state: Optional[State] = None):
        """Сбрасывает кэш промптов"""
        self.state_manager.take_out_cache(state)
    

    def reset_counter(self):
        """Сбрасывает счётчик сообщений"""
        self.state_manager.reset_counter()