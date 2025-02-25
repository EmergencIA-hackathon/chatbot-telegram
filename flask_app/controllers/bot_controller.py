import os
import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from flask_app.services.message_service import responder, start, callback
from flask_app.services.audio_service import handle_audio
from flask_app.services.location_service import receber_localizacao
from flask_app.services.image_service import handle_image
import asyncio

# Configuração do bot
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
application.add_handler(CallbackQueryHandler(callback))
application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
application.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))
application.add_handler(MessageHandler(filters.PHOTO, handle_image))

# Função de processamento de atualizações
async def processar_update(update: Update):
    print(f"Atualização recebida: {update}")  # Debug
    await application.initialize()
    await application.process_update(update)

# Função principal que roda o bot com o webhook
async def run_bot():
    """Inicializa e executa o bot de forma assíncrona"""
    print("Iniciando bot...")
    await application.initialize()
    await application.start()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply() 

    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
