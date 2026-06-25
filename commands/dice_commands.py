from vkbottle.bot import Message
from keyboard import KeyboardBuilder
from dices.dice import Dice
from dices.dice_manager import DiceManager


class DiceCommands:
    """Команды для бросков кубиков."""
    
    def __init__(self):
        self.dice_manager = DiceManager()
    
    def register(self) -> dict:
        """Регистрирует команды кубиков."""
        return {
            'dice': self.cmd_dice,
        }
    
    async def cmd_dice(self, message: Message, peer_id: int, text: str, session):
        """!dice — показать клавиатуру с кубиками"""
        self.dice_manager.clear(peer_id)
        await message.answer(
            "🎲 Выберите кубик для броска:",
            keyboard=KeyboardBuilder.get_dice_keyboard().get_json()
        )
    
    async def handle_payload(self, message: Message, peer_id: int, payload: dict) -> bool:
        """Обработка payload от кнопок кубиков."""
        if 'dice' not in payload and 'modifier' not in payload:
            return False
        
        # Сначала проверяем модификатор (бросок)
        if 'modifier' in payload and 'dice' in payload:
            modifier = payload['modifier']
            dice_type = payload['dice']
            
            result = Dice.roll(dice_type, modifier=modifier)
            response = Dice.format_result(result)
            
            self.dice_manager.clear(peer_id)
            
            await message.answer(
                response,
                parse_mode="html",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
            return True
        
        # Обработка кнопок кубиков
        dice_value = payload.get('dice')
        if not dice_value:
            return False
        
        # Отмена
        if dice_value == 'cancel':
            self.dice_manager.clear(peer_id)
            await message.answer(
                "Бросок кубика отменён",
                keyboard=KeyboardBuilder.get_main_keyboard().get_json()
            )
            return True
        
        # Назад к выбору кубика
        if dice_value == 'back':
            self.dice_manager.clear(peer_id)
            await message.answer(
                "Выберите кубик для броска:",
                keyboard=KeyboardBuilder.get_dice_keyboard().get_json()
            )
            return True
        
        # Выбор кубика
        if dice_value in Dice.DICE_TYPES.keys():
            self.dice_manager.select_dice(peer_id, dice_value)
            await message.answer(
                f"Выбран {dice_value}. Выберите модификатор:",
                keyboard=KeyboardBuilder.get_dice_modifier_keyboard(dice_value).get_json()
            )
            return True
        
        return False