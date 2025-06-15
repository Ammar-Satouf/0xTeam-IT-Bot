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
