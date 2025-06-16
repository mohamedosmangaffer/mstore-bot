import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

import sqlite3

DB_FILE = os.path.join(os.path.dirname(__file__), "../../orders.db")
USER_LANG = {}
USER_ORDER = {}
MENU, APP_SUB, ORDER_DETAILS = range(3)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

def get_lang(user_id): return USER_LANG.get(user_id, 'en')

async def handle_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE, rate_limiter) -> int:
    uid = update.effective_user.id
    if not rate_limiter.is_allowed(uid):
        await update.message.reply_text("🚫 يُرجى الانتظار قليلاً.")
        return MENU

    text = update.message.text
    lang = get_lang(uid)

    if text in ["📲 اشتراكات التطبيقات", "App Subscriptions"]:
        USER_ORDER[uid] = {"category": "apps"}
        reply = "🔽 اختر نوع الاشتراك:" if lang == 'ar' else "🔽 Select subscription:"
        kb = [
            ["Netflix", "ChatGPT"],
            ["YouTube Premium", "Spotify"],
            ["🔙 رجوع" if lang == 'ar' else "🔙 Back"]
        ]
        await update.message.reply_text(reply, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
        return APP_SUB

    await update.message.reply_text("❗ يرجى اختيار خيار صحيح من القائمة.")
    return MENU

async def handle_app_sub(update: Update, ctx: ContextTypes.DEFAULT_TYPE, rate_limiter) -> int:
    uid = update.effective_user.id
    if not rate_limiter.is_allowed(uid):
        await update.message.reply_text("🚫 يُرجى الانتظار قليلاً.")
        return APP_SUB

    if update.message.text in ["🔙 رجوع", "🔙 Back"]:
        from bot.handlers.menu import main_menu
        return await main_menu(update, ctx, rate_limiter)

    USER_ORDER[uid]["service"] = update.message.text
    lang = get_lang(uid)
    choice = update.message.text

    if lang == 'ar':
        msg = (
            f"📝 الرجاء إرسال تفاصيل الاشتراك في {choice} مثل:\n\n"
            "- البريد الإلكتروني المرتبط\n- الدولة\n- المدة المطلوبة\n- صورة إثبات الدفع (اختياري)"
        )
    else:
        msg = (
            f"📝 Please send subscription details for {choice}, such as:\n\n"
            "- Associated email\n- Country\n- Duration\n- Payment proof (optional)"
        )

    await update.message.reply_text(msg)
    return ORDER_DETAILS

async def handle_order_details(update: Update, ctx: ContextTypes.DEFAULT_TYPE, rate_limiter) -> int:
    uid = update.effective_user.id
    if not rate_limiter.is_allowed(uid):
        await update.message.reply_text("🚫 يُرجى الانتظار قليلاً.")
        return ORDER_DETAILS

    user = update.effective_user
    service = USER_ORDER.get(uid, {}).get("service", "Unknown")
    details = update.message.text
    lang = get_lang(uid)
    name = user.full_name
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_id = f"ORD-{uid}-{int(datetime.now().timestamp())}"

    # استقبال إثبات الدفع إن وُجد
    file_path = None
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_path = f"bot/receipts/{order_id}.jpg"
        await file.download_to_drive(file_path)

    order_msg = f\"\"\"\n📥 طلب جديد من المستخدم:\n👤 الاسم: {name}\n🆔 المعرف: {uid}\n📦 الخدمة: {service}\n🌐 اللغة: {'العربية' if lang == 'ar' else 'English'}\n🆔 رقم الطلب: {order_id}\n⏰ الوقت: {time_now}\n📝 التفاصيل:\n{details}\n\"\"\"
    if file_path:
        order_msg += f\"📎 تم إرفاق إثبات الدفع\n\"

    # حفظ في SQLite
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(\"INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)\", (uid, name, service, time_now, file_path, order_id, 'pending'))

    await ctx.bot.send_message(chat_id=ADMIN_ID, text=order_msg)
    await update.message.reply_text("✅ تم استلام طلبك بنجاح! سيتم التواصل معك قريبًا.")

    from bot.handlers.menu import main_menu
    return await main_menu(update, ctx, rate_limiter)
