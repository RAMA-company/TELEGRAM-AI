#!/usr/bin/env python3
"""
Professional AI Telegram Bot with OpenRouter
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI
import os

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AI_API_KEY = os.getenv('AI_API_KEY')  # این همون OpenRouter API Key تو هست

# AI Client for OpenRouter
class AIClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",  # ✅ OpenRouter endpoint
            api_key=AI_API_KEY,  # ✅ OpenRouter API Key
        )
    
    async def chat_completion(self, message: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://telegram-ai-bot.com",
                    "X-Title": "Telegram AI Bot",
                },
                model="google/gemini-flash-1.5-8b",  # ✅ مدل رایگان و پایدار
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"خطا در ارتباط با AI: {str(e)}"
    
    async def close(self):
        await self.client.close()

ai_client = AIClient()

# بقیه کد مثل قبل...
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AIBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self._start_handler))
        self.application.add_handler(CommandHandler("help", self._help_handler))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler)
        )
    
    async def _start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = """
🤖 ربات هوش مصنوعی

خوش آمدید! من ربات هوش مصنوعی شما هستم.

دستورات:
/start - نمایش این پیام
/help - راهنما

کافیست پیام بفرستید تا پاسخ دهم!
        """
        await update.message.reply_text(welcome_text)
    
    async def _help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
🆘 راهنما

• فقط پیام بفرستید تا پاسخ دهم
• می‌تونم در سوالات، برنامه‌نویسی، تحلیل و... کمک کنم

مثال:
- "پایتون یادم بده"
- "کد سی شارپ برای..."
- "در مورد هوش مصنوعی توضیح بده"
        """
        await update.message.reply_text(help_text)
    
    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        
        await update.message.chat.send_action(action="typing")
        
        try:
            ai_response = await ai_client.chat_completion(user_message)
            await update.message.reply_text(ai_response)
            logger.info(f"پیام کاربر {update.effective_user.id} پردازش شد")
        except Exception as e:
            logger.error(f"خطا در پردازش پیام: {e}")
            await update.message.reply_text("متاسفانه خطایی رخ داد. لطفا دوباره تلاش کنید.")
    
    def run(self):
        logger.info("ربات هوش مصنوعی فعال شد...")
        self.application.run_polling(drop_pending_updates=True)

async def cleanup():
    await ai_client.close()

def main():
    try:
        bot = AIBot()
        bot.run()
    except KeyboardInterrupt:
        print("ربات متوقف شد")
    except Exception as e:
        print(f"خطای جدی: {e}")
    finally:
        asyncio.run(cleanup())

if __name__ == "__main__":
    main()
