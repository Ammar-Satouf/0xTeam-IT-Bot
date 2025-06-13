import os
import asyncio
from flask import Flask, request
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, AIORateLimiter
from handlers import start, handle_message

app = Flask(_name_)
bot_app = None  # هنا بنخزن تطبيق التلغرام

@app.route("/")
def home():
    return "بوت تعليمي شغال بنجاح ✅"

async def run_bot():
    global bot_app
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("⚠ لم يتم العثور على التوكن في متغيرات البيئة")
        return

    bot_app = ApplicationBuilder()\
        .token(TOKEN)\
        .rate_limiter(AIORateLimiter())\
        .build()

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🚀 بدأ تشغيل البوت باستخدام polling")
    await bot_app.run_polling()

def start_flask():
    # شغل flask على البورت اللي منصوص عليه (مثلاً 8080)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # شغل flask في thread منفصل عشان ما يمنع asyncio من تشغيل البوت
    from threading import Thread
    flask_thread = Thread(target=start_flask)
    flask_thread.start()

    # شغل البوت (asyncio)
    asyncio.run(run_bot())
