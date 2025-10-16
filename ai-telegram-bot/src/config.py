import os 
from dataclasses import dataclass 
 
@dataclass 
class Config: 
    TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN') 
    AI_API_KEY: str = os.getenv('AI_API_KEY') 
    AI_BASE_URL: str = os.getenv('AI_BASE_URL', 'https://api.openai.com/v1') 
 
config = Config() 
