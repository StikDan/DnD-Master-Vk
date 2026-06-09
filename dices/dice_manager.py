from typing import Optional


class DiceManager:
    def __init__(self):
        self._dice_types: dict[int, str] = {}  # peer_id -> dice_type
        self._modifiers: dict[int, int] = {}   # peer_id -> modifier
    

    def select_dice(self, peer_id: int, dice_type: str) -> None:
        """Выбрать кубик для пользователя."""
        self._dice_types[peer_id] = dice_type
        self._modifiers[peer_id] = 0


    def set_modifier(self, peer_id: int, modifier: int) -> None:
        """Установить модификатор."""
        self._modifiers[peer_id] = modifier
    

    def get_selection(self, peer_id: int) -> Optional[str]:
        """Получить выбранный кубик."""
        return self._dice_types.get(peer_id)
    

    def get_modifier(self, peer_id: int) -> int:
        """Получить модификатор."""
        return self._modifiers.get(peer_id, 0)
    

    def clear(self, peer_id: int) -> None:
        """Сбросить выбор пользователя."""
        self._dice_types.pop(peer_id, None)
        self._modifiers.pop(peer_id, None)
    
    
    def has_selection(self, peer_id: int) -> bool:
        """Проверить, есть ли активный выбор."""
        return peer_id in self._dice_types