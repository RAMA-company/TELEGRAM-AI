import httpx 
import json 
from .config import config 
 
class AIClient: 
    def __init__(self): 
        self.api_key = config.AI_API_KEY 
        self.base_url = config.AI_BASE_URL 
        self.client = httpx.AsyncClient(timeout=30.0) 
 
    async def chat_completion(self, message: str) -
        headers = { 
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json" 
        } 
 
        payload = { 
            "model": "gpt-3.5-turbo", 
            "messages": [{"role": "user", "content": message}], 
            "max_tokens": 1000, 
            "temperature": 0.7 
        } 
 
        try: 
            response = await self.client.post( 
                f"{self.base_url}/chat/completions", 
                headers=headers, 
                json=payload 
            ) 
            response.raise_for_status() 
 
            data = response.json() 
            return data["choices"][0]["message"]["content"] 
 
        except httpx.HTTPError as e: 
            return f"🚫 API Error: {str(e)}" 
        except Exception as e: 
            return f"⚠️ Processing Error: {str(e)}" 
 
    async def close(self): 
        await self.client.aclose() 
 
ai_client = AIClient() 
