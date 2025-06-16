import os import asyncio from telegram.ext import ApplicationBuilder from dotenv import load_dotenv

from bot.handlers.start import conv_handler from bot.handlers.language import lang_cmd, help_cmd, menu_cmd from bot.middleware.rate_limiter import RateLimiter from bot.db.database import init_db

load_dotenv() TOKEN = os.getenv("BOT_TOKEN") ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

rate_limiter = RateLimiter(limit=3, window_seconds=10)

async def main(): app = ApplicationBuilder().token(TOKEN).build()

# Conversation flow
app.add_handler(conv_handler)

# Command handlers
app.add_handler(lang_cmd)
app.add_handler(help_cmd)
app.add_handler(menu_cmd)

# Initialize DB
init_db()

print("✅ M.store bot is running...")
await app.run_polling()

if name == "main": asyncio.run(main())

