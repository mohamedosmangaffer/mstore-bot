import os
import asyncio
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
import conv_handler
import lang_cmd, help_cmd, menu_cmd
import RateLimiter
import init_db

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

rate_limiter = RateLimiter(limit=3, window_seconds=10)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Conversation flow
    app.add_handler(conv_handler(rate_limiter))

    # Command handlers
    app.add_handler(lang_cmd(rate_limiter))
    app.add_handler(help_cmd(rate_limiter))
    app.add_handler(menu_cmd(rate_limiter))

    # Initialize DB
    init_db()

    print("✅ M.store bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
