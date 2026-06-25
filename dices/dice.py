import random


class Dice:
    DICE_TYPES = {
        'd4': 4,
        'd6': 6,
        'd8': 8,
        'd10': 10,
        'd12': 12,
        'd20': 20,
        'd100': 100,
    }
    
    DEFAULT_MODIFIERS = [-5, -3, -2, -1, 0, 1, 2, 3, 5]
    
    
    @classmethod
    def roll(cls, dice_type: str, count: int = 1, modifier: int = 0) -> dict:
        """
        Бросить кубики.
        
        Args:
            dice_type: Тип кубика (d4, d6, d8, d10, d12, d20, d100)
            count: Количество кубиков
            modifier: Модификатор к результату
            
        Returns:
            dict с результатами броска
        """
        if dice_type not in cls.DICE_TYPES:
            return {
                'success': False,
                'error': f'Неверный тип кубика: {dice_type}. Доступны: {", ".join(cls.DICE_TYPES.keys())}'
            }
        
        sides = cls.DICE_TYPES[dice_type]
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
    

    @classmethod
    def roll_d20(cls, modifier: int = 0) -> dict:
        """Бросок d20 с модификатором."""
        return cls.roll('d20', 1, modifier)
    

    @classmethod
    def format_result(cls, result: dict) -> str:
        """
        Форматирует результат броска в красивое сообщение.
        
        Args:
            result: Результат от roll()
            
        Returns:
            Отформатированная строка
        """
        if not result['success']:
            return f"❌ {result['error']}"
        
        response = (
            f"🎲 Бросок {result['dice_type']}\n\n"
            f"Результаты: {', '.join(map(str, result['rolls']))}\n"
        )
        
        if result['modifier'] != 0:
            sign = '+' if result['modifier'] > 0 else ''
            response += f"Модификатор: {sign}{result['modifier']}\n"
        
        response += f"Итого: {result['total']}"
        
        if result.get('is_crit'):
            response += "\n\n⭐ Критический успех!"
        elif result.get('is_fail'):
            response += "\n\n❌ Критический провал!"
        
        return response