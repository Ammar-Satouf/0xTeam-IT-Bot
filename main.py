import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, AIORateLimiter
from handlers import start, handle_message

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("⚠ لم يتم العثور على التوكن في متغيرات البيئة")
        return

    app = ApplicationBuilder()\
        .token(TOKEN)\
        .rate_limiter(AIORateLimiter())\
        .build()

    # إضافة معالجات الأوامر والرسائل
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # تشغيل البوت باستخدام polling
    print("🤖 البوت يعمل باستخدام polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
