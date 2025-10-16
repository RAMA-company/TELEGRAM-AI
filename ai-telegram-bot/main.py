#!/usr/bin/env python3 
 
import asyncio 
from src.bot import AIBot, cleanup 
 
def main(): 
    try: 
        bot = AIBot() 
        bot.run() 
    except KeyboardInterrupt: 
        print("\n🛑 Bot stopped by user") 
    except Exception as e: 
        print(f"❌ Fatal error: {e}") 
    finally: 
        asyncio.run(cleanup()) 
 
if __name__ == "__main__": 
    main() 
