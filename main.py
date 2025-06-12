from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message
import os

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.environ.get("PORT", "8443"))  # Render يعطي هذا تلقائياً
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")  # مسار سري يُفضل تغييره
    APP_URL = os.getenv("APP_URL")  # رابط تطبيقك على Render (بدون / في النهاية)

    if not TOKEN or not APP_URL:
        print("⚠ يرجى التأكد من وجود BOT_TOKEN و APP_URL في متغيرات البيئة.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print(f"✅ Webhook يعمل الآن على: {APP_URL}{WEBHOOK_PATH}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{APP_URL}{WEBHOOK_PATH}"
    )

if _name_ == "_main_":
    main()
