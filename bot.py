# bot.py – M.store (واجهة ثنائية اللغة + قائمة الخدمات)

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          MessageHandler, ConversationHandler, filters)

LANG, MENU = range(2)           # حالتا المحادثة
USER_LANG = {}                  # تخزين لغة كل مستخدم مؤقتاً

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """رسالة الترحيب باللغتين + اختيار اللغة."""
    txt = ("🔰 Welcome to M.store – Your Gateway to Premium Digital Services\n"
           "🔰 مرحبًا بك في متجر M.store – بوابتك للخدمات الرقمية المتميزة\n\n"
           "👇 Please select your preferred language to continue\n"
           "👇 يرجى اختيار لغتك المفضلة للمتابعة")
    kb = ReplyKeyboardMarkup([[KeyboardButton("🇸🇦 العربية"),
                               KeyboardButton("🇬🇧 English")]],
                             resize_keyboard=True)
    await update.message.reply_text(txt, reply_markup=kb)
    return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """يحفظ اللغة ويعرض القائمة الرئيسية المناسبة."""
    USER_LANG[update.effective_user.id] = 'ar' if "عرب" in update.message.text else 'en'
    return await main_menu(update, ctx)

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """يعرض القائمة الرئيسية حسب اللغة."""
    lang = USER_LANG.get(update.effective_user.id, 'en')
    if lang == 'ar':
        text = "🎯 مرحبًا بك في M.store\nاختر الخدمة التي تحتاجها:"
        menu = [["📲 اشتراكات التطبيقات", "🎮 خدمات الألعاب"],
                ["🚫 خدمات التخطي", "📦 أرشيف الخدمات"],
                ["📞 الدعم الفني", "🛒 طلب خاص"]]
    else:
        text = "🎯 Welcome to M.store\nSelect the service you need:"
        menu = [["📲 App Subscriptions", "🎮 Game Services"],
                ["🚫 Unlocking / Bypass", "📦 Archived Services"],
                ["📞 Technical Support", "🛒 Custom Request"]]

    await update.message.reply_text(text,
                                    reply_markup=ReplyKeyboardMarkup(menu,
                                                                     resize_keyboard=True))
    return MENU

async def handle_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """ردود تجريبية ثابتة لكل زر – سنستبدلها بربط API لاحقًا."""
    responses = {
        # عربي
        "📲 اشتراكات التطبيقات": "🟢 سيتم عرض خدمات الاشتراكات قريبًا.",
        "🎮 خدمات الألعاب": "🟢 سيتم عرض خدمات الألعاب قريبًا.",
        "🚫 خدمات التخطي": "🟢 خدمات التخطي ستُفعَّل لاحقًا.",
        "📦 أرشيف الخدمات": "📦 تم نقل بعض الخدمات هنا مؤقتًا.",
        "📞 الدعم الفني": "📞 تواصل معنا عبر @Mstore_support.",
        "🛒 طلب خاص": "📝 أرسل طلبك وسنرد عليك.",
        # English
        "📲 App Subscriptions": "🟢 Subscription services coming soon.",
        "🎮 Game Services": "🟢 Game services coming soon.",
        "🚫 Unlocking / Bypass": "🟢 Unlocking services will be available soon.",
        "📦 Archived Services": "📦 Some services are archived temporarily.",
        "📞 Technical Support": "📞 Contact @Mstore_support.",
        "🛒 Custom Request": "📝 Send your custom request and we will respond."
    }
    reply = responses.get(update.message.text,
                          "❗ خدمة غير معروفة" if USER_LANG.get(update.effective_user.id)=='ar'
                          else "❗ Unknown option.")
    await update.message.reply_text(reply)
    return MENU

# ===== تشغيل البوت =====
if __name__ == "__main__":
    import os, asyncio
    TOKEN = os.getenv("BOT_TOKEN")          # أضف المتغيّر في إعدادات Render
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)]
        },
        fallbacks=[]
    )
    app.add_handler(conv)

    print("✅ M.store bot is running...")
    asyncio.run(app.run_polling())
