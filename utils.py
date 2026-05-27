from config import Config


class Utils:

    @staticmethod
    async def send_split(bot, peer_id: int, text: str, max_length: int = 4000):
        """Разбивает длинный текст на части и отправляет в ВК"""
        while text:
            chunk = text[:max_length]
            await bot.api.messages.send(
                peer_id=peer_id,
                message=chunk,
                random_id=0
            )
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