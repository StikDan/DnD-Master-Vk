import random


class Utils:

    @staticmethod
    async def send_split(bot, peer_id: int, text: str, max_length: int = 4000, keyboard=None):
        """
        Разбивает длинный текст на части и отправляет в ВК.
        
        Args:
            bot: Экземпляр бота
            peer_id: ID получателя
            text: Текст сообщения
            max_length: Максимальная длина одного сообщения
            keyboard: Объект Keyboard (опционально)
        """
        keyboard_json = keyboard.get_json() if keyboard else None
        
        while text:
            chunk = text[:max_length]
            
            params = {
                'peer_id': peer_id,
                'message': chunk,
                'random_id': 0
            }
            
            if keyboard_json:
                params['keyboard'] = keyboard_json
                keyboard_json = None
            
            await bot.api.messages.send(**params)
            
            text = text[max_length:]


    @staticmethod
    def map_role(role: str) -> str:
        """Преобразует кастомную роль в формат Ollama API."""
        role = role.lower()
        if "игрок" in role or role == "user":
            return "user"
        elif "мастер" in role or role == "assistant":
            return "assistant"
        elif role == "system":
            return "system"
        return "user"
    

    @staticmethod
    def roll_dice(dice_type: str, count: int = 1, modifier: int = 0) -> dict:
        """
        Бросить кубики DnD.
        
        Args:
            dice_type: Тип кубика (d4, d6, d8, d10, d12, d20, d100)
            count: Количество кубиков
            modifier: Модификатор к результату
            
        Returns:
            dict с результатами броска
        """
        DICE_TYPES = {
            'd4': 4,
            'd6': 6,
            'd8': 8,
            'd10': 10,
            'd12': 12,
            'd20': 20,
            'd100': 100,
        }
        
        if dice_type not in DICE_TYPES:
            return {
                'success': False,
                'error': f'Неверный тип кубика: {dice_type}. Доступны: {", ".join(DICE_TYPES.keys())}'
            }
        
        sides = DICE_TYPES[dice_type]
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls) + modifier
        
        return {
            'success': True,
            'dice_type': dice_type,
            'count': count,
            'modifier': modifier,
            'rolls': rolls,
            'total': total,
            'natural_roll': rolls[0] if count == 1 else None,
            'is_crit': rolls[0] == sides if count == 1 and dice_type == 'd20' else False,
            'is_fail': rolls[0] == 1 if count == 1 and dice_type == 'd20' else False,
        }


    @staticmethod
    def format_dice_result(result: dict) -> str:
        """
        Форматирует результат броска в красивое сообщение.
        
        Args:
            result: Результат от roll_dice()
            
        Returns:
            Отформатированная строка
        """
        if not result['success']:
            return f"❌ {result['error']}"
        
        response = (
            f"🎲 <b>Бросок {result['dice_type']}</b>\n\n"
            f"Результаты: {', '.join(map(str, result['rolls']))}\n"
            f"<b>Итого: {result['total']}</b>"
        )
        
        if result.get('is_crit'):
            response += "\n\n⭐ <b>Критический успех!</b>"
        elif result.get('is_fail'):
            response += "\n\n❌ <b>Критический провал!</b>"
        
        return response