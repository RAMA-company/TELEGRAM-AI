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
from dataclasses import dataclass

# Configuration
@dataclass
class Config:
    TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
    AI_API_KEY: str = os.getenv('AI_API_KEY')

config = Config()

# AI Client for OpenRouter
class AIClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=config.AI_API_KEY,
        )
    
    async def chat_completion(self, message: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://telegram-ai-bot.com",
                    "X-Title": "Telegram AI Bot",
                },
                model="deepseek/deepseek-r1:free",  # Using the free model you specified
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
            return f"I apologize, but I encountered an error: {str(e)}"
    
    async def close(self):
        await self.client.close()

ai_client = AIClient()

# Bot setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AIBot:
    def __init__(self):
        self.application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self._start_handler))
        self.application.add_handler(CommandHandler("help", self._help_handler))
        self.application.add_handler(CommandHandler("models", self._models_handler))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler)
        )
    
    async def _start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = """
🤖 AI Assistant Bot (Powered by OpenRouter)

Welcome! I'm your professional AI assistant using DeepSeek R1.

Available Commands:
/start - Show this welcome message
/help - Get assistance
/models - Show available AI models

Simply send me a message and I'll respond with AI-powered insights!
        """
        await update.message.reply_text(welcome_text)
    
    async def _help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
🆘 Help Guide

• Just type your message and I'll respond
• I can help with questions, writing, analysis, and more
• Uses DeepSeek R1 model (free)

Examples:
- "Explain quantum computing"
- "Write a Python function"
- "Help me plan a project"
- "Translate this text"
        """
        await update.message.reply_text(help_text)
    
    async def _models_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        models_info = """
🤖 Available AI Models:

Current: deepseek/deepseek-r1:free (Free)

Other popular models:
- anthropic/claude-3.5-sonnet
- google/gemini-flash-1.5-8b
- meta-llama/llama-3.1-8b-instruct
- openai/gpt-4o-mini

Change the model in the code if needed!
        """
        await update.message.reply_text(models_info)
    
    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        
        # Show typing action
        await update.message.chat.send_action(action="typing")
        
        try:
            ai_response = await ai_client.chat_completion(user_message)
            await update.message.reply_text(ai_response)
            logger.info(f"Processed message from user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text("Sorry, I encountered an error processing your request. Please try again.")
    
    def run(self):
        logger.info("Starting AI Telegram Bot with OpenRouter...")
        self.application.run_polling(drop_pending_updates=True)

async def cleanup():
    await ai_client.close()

def main():
    try:
        bot = AIBot()
        bot.run()
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        asyncio.run(cleanup())

if __name__ == "__main__":
    main()
