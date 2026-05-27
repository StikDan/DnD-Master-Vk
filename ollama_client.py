import os
import aiohttp
from dotenv import load_dotenv
from conversation_history import ConversationHistory
from utils import Utils
from config import Config


load_dotenv()

class OllamaClient:
    def __init__(self, system_prompt: str | None = None):
        self.config = Config()
        self.model = os.environ.get('OLLAMA_MODEL', '')
        
        if system_prompt:
            self.system_prompt = system_prompt
        else:
            prompt_file = os.environ.get('PROMPT_FILE', 'systemPrompt.md')
            self.system_prompt = ConversationHistory.load_prompt(prompt_file)
        
        self.url = "http://localhost:11434/api/chat"
        self.headers = {"Content-Type": "application/json"}

    def _build_messages(self, user_message: str, history: list) -> list:
        messages = []
        
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        limit = self.config.MEMORY_PAIR
        for msg in (history[-limit:] if limit else history):
            if isinstance(msg, dict):
                role = Utils.map_role(msg.get("role", ""))
                content = msg.get("content", "")
                if role and content:
                    messages.append({"role": role, "content": content})
        
        if user_message and user_message.strip():
            messages.append({"role": "user", "content": user_message.strip()})
        
        return messages


    async def get_response(self, user_message: str, history: list):
        if not self.model:
            raise ValueError("Не выбрана модель Ollama.")
        
        messages = self._build_messages(user_message, history)

        #ОТЛАДКА
        print(f"История получена: {len(history)} записей")
        for i, msg in enumerate(history[-10:]):
            if isinstance(msg, dict):
                role = msg.get('role', '?')
                content_preview = msg.get('content', '')[:60].replace('\n', ' ')
                print(f"   [{i+1}] {role}: {content_preview}...")
        print(f"Всего сообщений в запросе: {len(messages)}")

        data = {
            "model": self.model,
            "messages": messages,
            "options": {
                "num_ctx": self.config.NUM_CTX,
                "num_predict": self.config.NUM_PREDICT,
                "temperature": self.config.TEMPERATURE,
                "top_p": self.config.TOP_P,
            },
            "stream": False
        }

        print('Отправляем в Ollama...')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, json=data) as resp:
                    print(f"Статус ответа: {resp.status}")
                    
                    if resp.status != 200:
                        error_body = await resp.text()
                        print(f"Ошибка {resp.status}: {error_body[:1000]}")
                        return f"API вернуло {resp.status}: {error_body[:200]}"
                    
                    result = await resp.json()
                    content = result.get("message", {}).get("content", "")
                    
                    if not content:
                        print("Ответ пустой!")
                        return "Нейросеть вернула пустой ответ."
                    
                    return content
                    
        except Exception as e:
            print(f"Ошибка: {e}")
            return f"Ошибка: {e}"