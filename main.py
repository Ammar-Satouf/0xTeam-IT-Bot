from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message

TOKEN = "YOUR_BOT_TOKEN_HERE"

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
