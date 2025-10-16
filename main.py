#!/usr/bin/env python3
"""
Professional AI Telegram Bot
Main entry point
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import httpx
import os
from dataclasses import dataclass

# Configuration
@dataclass
class Config:
    TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
    AI_API_KEY: str = os.getenv('AI_API_KEY')
    AI_BASE_URL: str = os.getenv('AI_BASE_URL', 'https://api.openai.com/v1')

config = Config()

# AI Client
class AIClient:
    def __init__(self):
        self.api_key = config.AI_API_KEY
        self.base_url = config.AI_BASE_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def chat_completion(self, message: str) -> str:
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
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Processing Error: {str(e)}"
    
    async def close(self):
        await self.client.aclose()

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
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler)
        )
    
    async def _start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = """
AI Assistant Bot

Welcome! I'm your professional AI assistant powered by advanced language models.

Available Commands:
/start - Show this welcome message
/help - Get assistance

Simply send me a message and I'll respond with AI-powered insights!
        """
        await update.message.reply_text(welcome_text)
    
    async def _help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
Help Guide

• Just type your message and I'll respond
• I can help with questions, writing, analysis, and more
• Keep messages under 2000 characters for best results

Examples:
- "Explain quantum computing"
- "Write a Python function for..."
- "Help me plan a project"

For technical issues, contact the administrator.
        """
        await update.message.reply_text(help_text)
    
    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        
        await update.message.chat.send_action(action="typing")
        
        try:
            ai_response = await ai_client.chat_completion(user_message)
            await update.message.reply_text(f"{ai_response}")
            logger.info(f"Processed message from user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text("Sorry, I encountered an error processing your request. Please try again.")
    
    def run(self):
        logger.info("Starting AI Telegram Bot...")
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
