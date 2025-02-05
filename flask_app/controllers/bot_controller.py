from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
from config import TOKEN
from services.message_service import responder, start, callback
from services.audio_service import handle_audio
from services.location_service import pedir_localizacao, receber_localizacao

async def main(update: Update):
    app = Application.builder().token(TOKEN).build()
    await app.initialize() 

    # Adicionando handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📍 Compartilhar Localização"), pedir_localizacao))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))

    print("Bot está processando a atualização...")

    await app.process_update(update)

    webhook_url = "https://14ee-177-85-89-185.ngrok-free.app/webhook"
    app.bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    pass
