import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from services.message_service import responder, start, callback
from services.audio_service import handle_audio
from services.location_service import receber_localizacao
from services.image_service import handle_image


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


application = Application.builder().token(TOKEN).build()


# Adicionando handlers apenas uma vez
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
application.add_handler(CallbackQueryHandler(callback))
application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
application.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))
application.add_handler(MessageHandler(filters.PHOTO, handle_image))


async def processar_update(update):
   await application.initialize()
   await application.process_update(update)


async def start_bot():
   """Inicializa e executa o bot"""
   print("Iniciando bot...")
   await application.initialize()
   await application.start()
   print("Bot iniciado!")


if __name__ == "__main__":
   import asyncio
   asyncio.run(start_bot())