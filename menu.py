from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

USER_LANG = {}
USER_ORDER = {}

MENU, APP_SUB = range(2)

def get_lang(user_id): return USER_LANG.get(user_id, 'en')

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE, rate_limiter) -> int:
    uid = update.effective_user.id
    if not rate_limiter.is_allowed(uid):
        await update.message.reply_text("🚫 يُرجى الانتظار قليلاً.")
        return MENU

    lang = get_lang(uid)
    if lang == 'ar':
        txt = (
            "🎯 مرحبًا بك في قائمة خدمات M.store\n"
            "✅ جميع الخدمات موثوقة ومجربة\n\n"
            "📞 للتواصل والدعم:\n"
            "Telegram: https://t.me/Mstore_bot_support\n"
            "WhatsApp: +249965812441"
        )
        menu = [
            ["🔐 خدمات الهواتف وتخطي الحمايات"],
            ["📲 اشتراكات التطبيقات", "🎮 خدمات الألعاب"],
            ["🛰️ اشتراك ستارلينك"], ["📦 الخدمات المتوقفة حاليًا"],
            ["📞 الدعم الفني", "💬 الملاحظات وآراء العملاء"]
        ]
    else:
        txt = (
            "🎯 Welcome to M.store Services Menu\n"
            "✅ All services are trusted and verified\n\n"
            "📞 Contact Support:\n"
            "Telegram: https://t.me/Mstore_bot_support\n"
            "WhatsApp: +249965812441"
        )
        menu = [
            ["🔐 Phones & Unlocking Services"],
            ["📲 App Subscriptions", "🎮 Game Services"],
            ["🛰️ Starlink Subscription"], ["📦 Archived Services"],
            ["📞 Technical Support", "💬 Feedback"]
        ]
    await update.message.reply_text(txt, reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True))
    return MENU
