from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

LANG, MENU = range(2)
USER_LANG = {}

def get_lang(user_id): return USER_LANG.get(user_id, 'en')

def conv_handler(rate_limiter):
    async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_user.id
        if not rate_limiter.is_allowed(uid):
            await update.message.reply_text("🚫 يُرجى الانتظار قليلاً قبل إعادة المحاولة.")
            return ConversationHandler.END

        txt = (
            "🔰 Welcome to M.store – Your Gateway to Premium Digital Services\n"
            "🔰 مرحبًا بك في متجر M.store – بوابتك للخدمات الرقمية المتميزة\n\n"
            "👇 Please select your preferred language to continue\n"
            "👇 يرجى اختيار لغتك المفضلة للمتابعة"
        )
        kb = [["🇸🇦 العربية", "🇬🇧 English"]]
        await update.message.reply_text(txt, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        return LANG

    async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
        uid = update.effective_user.id
        lang = 'ar' if "عرب" in update.message.text else 'en'
        USER_LANG[uid] = lang
        await update.message.reply_text("✅ Language set. Use /menu to start.")
        return MENU

    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
        },
        fallbacks=[],
    )
