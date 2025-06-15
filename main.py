from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message, notify_update_to_users
import os
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")


async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started...")
    await application.run_polling()


if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    keep_alive()

    nest_asyncio.apply()

    asyncio.run(main())


def check_secrets():
    token = os.getenv("TOKEN")
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    if not token:
        print("⚠️ TOKEN is not set in secrets.")
    else:
        print("✅ TOKEN is set.")

    if not mongo_uri:
        print("⚠️ MONGO_URI is not set in secrets.")
    else:
        print("✅ MONGO_URI is set.")

    if not mongo_db_name:
        print(
            "⚠️ MONGO_DB_NAME is not set in secrets, using default value 'telegram_bot_db'."
        )
    else:
        print("✅ MONGO_DB_NAME is set.")

check_secrets()
