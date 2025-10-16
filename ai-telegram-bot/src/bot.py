import logging 
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 
from .config import config 
from .ai_client import ai_client 
 
logging.basicConfig( 
    format='%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s', 
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
        ) 
 
    async def _start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE): 
🤖 **AI Assistant Bot** 🚀 
 
Welcome! I'm your professional AI assistant powered by advanced language models. 
 
**Available Commands:** 
/start - Show this welcome message 
/help - Get assistance 
 
Simply send me a message and I'll respond with AI-powered insights! 
        await update.message.reply_text(welcome_text, parse_mode='Markdown') 
 
    async def _help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE): 
🆘 **Help Guide** 
 
• Just type your message and I'll respond 
• I can help with questions, writing, analysis, and more 
• Keep messages under 2000 characters for best results 
 
**Examples:** 
- "Explain quantum computing" 
- "Write a Python function for..." 
- "Help me plan a project" 
 
For technical issues, contact the administrator. 
        await update.message.reply_text(help_text, parse_mode='Markdown') 
 
    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE): 
        user_message = update.message.text 
        await update.message.chat.send_action(action="typing") 
 
        try: 
            ai_response = await ai_client.chat_completion(user_message) 
            await update.message.reply_text(f"🤖 {ai_response}", parse_mode='Markdown') 
            logger.info(f"Processed message from user {update.effective_user.id}") 
        except Exception as e: 
            logger.error(f"Error processing message: {e}") 
            await update.message.reply_text("❌ Sorry, I encountered an error processing your request. Please try again.") 
 
    def run(self): 
        logger.info("Starting AI Telegram Bot...") 
        self.application.run_polling(drop_pending_updates=True) 
 
async def cleanup(): 
    await ai_client.close() 
 
if __name__ == "__main__": 
    bot = AIBot() 
    bot.run() 
