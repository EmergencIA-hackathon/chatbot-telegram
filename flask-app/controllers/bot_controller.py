import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
from config import TOKEN
from services.message_service import responder, start, callback
from services.audio_service import handle_audio
from services.location_service import pedir_localizacao, receber_localizacao

def main():
    app = Application.builder().token(TOKEN).build()

    # Adicionando handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📍 Compartilhar Localização"), pedir_localizacao))
    app.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))

    print("Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
