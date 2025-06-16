from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

USER_LANG = {}  # شارك هذا عبر ملف مشترك أو Context عند التوسع

def get_lang(user_id): return USER_LANG.get(user_id, 'en')

def lang_cmd(rate_limiter):
    async def handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if not rate_limiter.is_allowed(uid):
            await update.message.reply_text("🚫 يُرجى الانتظار قليلاً.")
            return
        from bot.handlers.start import conv_handler
        await conv_handler(rate_limiter).entry_points[0].callback(update, ctx)

    return CommandHandler("lang", handler)

def help_cmd(rate_limiter):
    async def handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if not rate_limiter.is_allowed(uid):
            await update.message.reply_text("🚫 يُرجى الانتظار قليلاً.")
            return
        lang = get_lang(uid)
        msg = (
            "ℹ️ الأوامر المتاحة:\n"
            "/lang – تغيير اللغة\n"
            "/menu – القائمة الرئيسية\n"
            "/help – عرض المساعدة"
            if lang == 'ar' else
            "ℹ️ Available commands:\n"
            "/lang – Change language\n"
            "/menu – Main menu\n"
            "/help – Show help"
        )
        await update.message.reply_text(msg)

    return CommandHandler("help", handler)

def menu_cmd(rate_limiter):
    async def handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        from bot.handlers.menu import main_menu
        await main_menu(update, ctx, rate_limiter)

    return CommandHandler("menu", handler)
