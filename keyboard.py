from vkbottle.tools import Keyboard, KeyboardButtonColor, Text


class KeyboardBuilder:
    
    @staticmethod
    def get_main_keyboard() -> Keyboard:
        """Основная клавиатура с командами"""
        keyboard = (
            Keyboard(one_time=False, inline=False)
            .add(Text("📜 Новая сессия", payload={"command": "session new"}), color=KeyboardButtonColor.SECONDARY)
            .add(Text("📋 Список сессий", payload={"command": "session list"}), color=KeyboardButtonColor.SECONDARY)
            .row()

            .add(Text("🔗 Присоединиться", payload={"command": "session join"}), color=KeyboardButtonColor.SECONDARY)
            .row()

            .add(Text("🔄 Повторить", payload={"command": "retry"}), color=KeyboardButtonColor.SECONDARY)
            .add(Text("🎲 Кубики", payload={"command": "dice"}), color=KeyboardButtonColor.PRIMARY)
            .row()
            
            .add(Text("ℹ️ Команды", payload={"command": "commands"}), color=KeyboardButtonColor.PRIMARY)
        )
        
        return keyboard


    @staticmethod
    def get_dice_keyboard() -> Keyboard:
        """Клавиатура с кубиками DnD"""
        keyboard = (
            Keyboard(one_time=False, inline=True)
            .add(Text("🎲 d4", payload={"dice": "d4"}), color=KeyboardButtonColor.POSITIVE)
            .add(Text("🎲 d6", payload={"dice": "d6"}), color=KeyboardButtonColor.POSITIVE)
            .add(Text("🎲 d8", payload={"dice": "d8"}), color=KeyboardButtonColor.POSITIVE)
            .row()
            
            .add(Text("🎲 d10", payload={"dice": "d10"}), color=KeyboardButtonColor.POSITIVE)
            .add(Text("🎲 d12", payload={"dice": "d12"}), color=KeyboardButtonColor.POSITIVE)
            .add(Text("🎲 d20", payload={"dice": "d20"}), color=KeyboardButtonColor.PRIMARY)
            .row()
            
            .add(Text("🎲 d100", payload={"dice": "d100"}), color=KeyboardButtonColor.POSITIVE)
            .row()
            
            .add(Text("Отмена", payload={"dice": "cancel"}), color=KeyboardButtonColor.NEGATIVE)
        )
        
        return keyboard
    

    @staticmethod
    def get_dice_modifier_keyboard(dice_type: str) -> Keyboard:
        """Клавиатура с модификаторами"""
        keyboard = (
            Keyboard(one_time=False, inline=True)
            .add(Text("-5", payload={"modifier": -5, "dice": dice_type}), color=KeyboardButtonColor.NEGATIVE)
            .add(Text("-3", payload={"modifier": -3, "dice": dice_type}), color=KeyboardButtonColor.NEGATIVE)
            .add(Text("-2", payload={"modifier": -2, "dice": dice_type}), color=KeyboardButtonColor.NEGATIVE)
            .row()
            
            .add(Text("-1", payload={"modifier": -1, "dice": dice_type}), color=KeyboardButtonColor.NEGATIVE)
            .add(Text("0", payload={"modifier": 0, "dice": dice_type}), color=KeyboardButtonColor.SECONDARY)
            .add(Text("+1", payload={"modifier": 1, "dice": dice_type}), color=KeyboardButtonColor.POSITIVE)
            .row()
            
            .add(Text("+2", payload={"modifier": 2, "dice": dice_type}), color=KeyboardButtonColor.POSITIVE)
            .add(Text("+3", payload={"modifier": 3, "dice": dice_type}), color=KeyboardButtonColor.POSITIVE)
            .add(Text("+5", payload={"modifier": 5, "dice": dice_type}), color=KeyboardButtonColor.POSITIVE)
            .row()
            
            .add(Text("Назад", payload={"dice": "back"}), color=KeyboardButtonColor.SECONDARY)
        )
        
        return keyboard