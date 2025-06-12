from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from handlers import start, handle_message
import os
import asyncio

PORT = int(os.environ.get("PORT", 8443))  # يستخدمه Render
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # رابط موقعك على Render (بصيغة https://your-app-name.onrender.com)

async def main():
    if not TOKEN or not WEBHOOK_URL:
        print("⚠ تأكد من وجود BOT_TOKEN و WEBHOOK_URL في متغيرات البيئة")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.start()
    await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    print("✅ البوت يعمل باستخدام Webhook...")
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
