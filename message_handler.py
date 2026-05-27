from conversation_history import ConversationHistory
from config import Config
from db.Modules import factory_importer
from vkbottle.bot import Message


class MessageHandler:
    def __init__(self, config: Config, history: ConversationHistory):
        self.config = config
        self.history = history
        self.import_module = factory_importer


    async def _retry_message(self):
        """Откатить последних 2 сообщения"""
        await self.history.delete_message(count_msg=2)


    async def handle_command(self, message: Message) -> bool:
        """
        Обработка команд. Возвращает True, если команда распознана и обработана.
        Возвращает False, если это обычное сообщение.
        """
        text = message.text or ""
        text = text.lower()
        
        if not text.startswith(self.config.IGNORE_PREFIX):
            return False

        # !clear — очистить историю
        if text == self.config.IGNORE_PREFIX + 'clear':
            await self.history.clear_history()
            await message.answer('История очищена!')
            return True

        # !retry — откатить последний запрос
        if text == self.config.IGNORE_PREFIX + 'retry':
            await self._retry_message()
            await message.answer('Откат выполнен!')
            return True

        # !commands — список команд
        if text == self.config.IGNORE_PREFIX + 'commands':
            await message.answer('''Список команд:
`!clear` — очистить историю
`!retry` — откатить последний запрос
`!import-history` — импортировать текущую историю в базу данных
`!import-npcs` — импортировать все NPC в базу данных
`!commands` — список команд''')
            return True

        # !import-history — импорт истории
        if text == self.config.IGNORE_PREFIX + 'import-history':
            importer = self.import_module.get_importer("history")
            result = await importer.import_data(self.config.HISTORY_FILE)
            await message.answer(result)
            return True

        # !import-npcs — импорт NPC
        if text == self.config.IGNORE_PREFIX + 'import-npcs':
            importer = self.import_module.get_importer("npc")
            result = await importer.import_from_folder("data/NPC")
            await message.answer(result)
            return True
        
        return True