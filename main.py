import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, AIORateLimiter
from handlers import start, handle_message

async def on_startup(app):
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await app.bot.set_webhook(url=webhook_url)
        print("✅ تم إعداد الـ Webhook بنجاح!")
    else:
        print("⚠ لم يتم تحديد WEBHOOK_URL")

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("⚠ لم يتم العثور على التوكن في متغيرات البيئة")
        return

    app = ApplicationBuilder()\
        .token(TOKEN)\
        .rate_limiter(AIORateLimiter())\
        .build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # إعداد الـ webhook قبل التشغيل
    await on_startup(app)

    # تشغيل الـ webhook مع الإعدادات
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        webhook_url=os.getenv("WEBHOOK_URL")
    )

if _name_ == "_main_":
    # تشغيل الحدث الرئيسي بشكل آمن لتجنب خطأ loop is already running
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is running" in str(e):
            print("⚠ حدث خطأ: الحلقة الحدثية تعمل بالفعل")
        else:
            raise
