from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import AIORateLimiter
from handlers import start, handle_message
import os

async def on_startup(app):
    webhook_url = os.getenv("WEBHOOK_URL")
    await app.bot.set_webhook(url=webhook_url)
    print("✅ تم إعداد الـ Webhook بنجاح!")

def main():
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

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=os.getenv("WEBHOOK_URL"),
        on_startup=on_startup
    )

if __name__ == "__main__":
    main()
