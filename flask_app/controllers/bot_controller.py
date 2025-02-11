from telegram import Update
import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from services.message_service import responder, start, callback
from services.audio_service import handle_audio
from services.location_service import receber_localizacao

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main(update: Update, app: Application):
    # Adicionando handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))

    print("Bot está processando a atualização...")

    await app.process_update(update)

if __name__ == "__main__":
    pass
